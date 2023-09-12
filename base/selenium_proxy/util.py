from pydash import _
from selenium.webdriver.common.by import By


def is_valid_by(by):
    for attr in dir(By):
        if by == getattr(By, attr):
            return True
    return False


def is_valid(locator):
    """
    Check whether the locator is valid.

    Args:
        locator(dict || list || tuple): locator

    Returns:
        Boolean
    """
    if isinstance(locator, (tuple, list)):
        if len(locator) != 2:
            return False
        if not is_valid_by(locator[0]):
            return False
        if not isinstance(locator[1], str):
            return False
        return True

    if isinstance(locator, dict):
        by = None
        for key in locator:
            if is_valid_by(key):
                if by is None:
                    by = key
                else:
                    return False
        if by is None:
            return False
        return True

    return False


def solve(locator, *args):
    """
    Replace the %s in the locator with true value.

    Args:
        locator(dict || list || tuple): locator

    Returns:
        Tuple(by, value) | Dict(by: value):
    """
    if isinstance(locator, str):
        return locator % args

    if not is_valid(locator):
        raise Exception("Invalid locator", locator)

    if isinstance(locator, (tuple, list)):
        return locator[0], locator[1] % args

    if isinstance(locator, dict):
        by = None
        for key in locator:
            if is_valid_by(key):
                by = key
                break
        return _.defaults({by: locator[by] % args}, locator)
    return None


def to_tuple(locator):
    """
    Convert the locator param to tuple.

    Args:
        locator(dict || list || tuple): locator

    Returns:
        Tuple(by, value):
    """
    if isinstance(locator, str):
        is_css = ">" in locator and ("/" not in locator)
        is_xpath = "/" in locator
        if is_css is True and is_xpath is True:
            raise Exception("Invalid locator", locator)
        if is_xpath:
            return By.XPATH, locator
        return By.CSS_SELECTOR, locator

    if not is_valid(locator):
        raise Exception("Invalid locator", locator)

    if isinstance(locator, (tuple, list)):
        return locator[0], locator[1]

    raise Exception("Invalid locator", locator)


def solve_to_tuple(locator, *args):
    """
    Replace the %s in the locator with true value, and return tuple.

    Args:
        locator(dict || list || tuple): locator

    Returns:
        Tuple(by, value):
    """
    if isinstance(locator, str):
        return By.XPATH, locator % args

    if not is_valid(locator):
        raise Exception("Invalid locator", locator)

    for item in args:
        if not isinstance(item, str):
            raise Exception("Value should be string.", item)

    if isinstance(locator, (tuple, list)):
        return locator[0], locator[1] % args

    if isinstance(locator, dict):
        by = None
        for key in locator:
            if is_valid_by(key):
                by = key
                break
        return by, locator[by] % args
    return None


def check_value(target, check):
    if not isinstance(target, str):
        raise Exception("Check target should be a str.", target)
    if not isinstance(check, dict):
        raise Exception("Check body should be a dict.", check)

    for key in check:
        if key == "tag":
            continue
        if key not in ["eq", "start", "end", "contain", "not_contain"]:
            raise Exception("Unsupported check type.", key)

        if key == "eq" and not __eq(target, check[key]):
            raise Exception("Check equal fail.", target, check[key])
        if key == "start" and not __start(target, check[key]):
            raise Exception("Check starts with fail.", target, check[key])
        if key == "end" and not __end(target, check[key]):
            raise Exception("Check ends with fail.", target, check[key])
        if key == "contain" and not __contain(target, check[key]):
            raise Exception("Check contain fail.", target, check[key])
        if key == "not_contain" and not __not_contain(target, check[key]):
            raise Exception("Check contain fail.", target, check[key])


def __start(target, values):
    """
    Check a string value if it starts with any string in the `values` list

    Args:
        target(str || unicode): The value to check.
        values(str || list[str]): The value str or value list to use.

    Returns:
        Boolean: True if pass; False if fail.
    """
    for value in _.maybe_to_list(values):
        if target.startswith(value):
            return True
    return False


def __end(target, values):
    """
    Check a string value if it ends with any string in the `values` list

    Args:
        target(str || unicode): The value to check.
        values(str || list[str]): The value str or value list to use.

    Returns:
        Boolean: True if pass; False if fail.
    """
    for value in _.maybe_to_list(values):
        if target.endswith(value):
            return True
    return False


def __eq(target, values):
    """
    Check a string value if it equals any string in the `values` list

    Args:
        target(str || unicode): The value to check.
        values(str || list[str]): The value str or value list to use.

    Returns:
        Boolean: True if pass; False if fail.
    """
    for value in _.maybe_to_list(values):
        if target == value:
            return True
    return False


def __contain(target, values):
    """
    Check a string value if it contains any string in the `values` list

    Args:
        target(str || unicode): The value to check.
        values(str || list[str]): The value str or value list to use.

    Returns:
        Boolean: True if pass; False if fail.
    """
    for value in _.maybe_to_list(values):
        if value in target:
            return True
    return False


def __not_contain(target, values):
    """
    Check a string value if it does not contain any string in the `values` list

    Args:
        target(str || unicode): The value to check.
        values(str || list[str]): The value str or value list to use.

    Returns:
        Boolean: True if pass; False if fail.
    """
    for value in _.maybe_to_list(values):
        if value not in target:
            return True
    return False
