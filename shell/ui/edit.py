from pydash import _
import time
from selenium.common.exceptions import NoSuchElementException

from .. import ui
from ...base.exceptions import GenericException
from ...base.exceptions.control import ValidationException, ControlNotFoundException
from ...base.exceptions.element import ElementNotVisibleException
from .dialog import AbstractDialog
from ..web_elements.checkbox import CheckBoxList, CheckBox
from ..web_elements.date_picker import DatePicker
from ..web_elements.dropdown import DropDown, MultiSelectDropDown
from ..web_elements.input import Input
from ..web_elements.radio import Radio, RadioOption, RadioCbu
from ..web_elements.text_area import TextArea
from ...base.exceptions import TAEditFormException
from .table import Table
from ..web_elements.checkbox import CheckBoxValue,CheckBoxSelect


class Edit:


    CONTENT = "//mat-card/mat-card-content"
    FORM_FIX = "/form"
    ENTRY = "/div/div/div[./label[contains(text(),'{}')]]"
    LOADER = "//div[@class='ngx-overlay loading-foreground']"
    BUTTON = "//mat-card/div/button[./span[contains(text(),'Next')]]"
    SAVE_AS_DRAFT = "//mat-card/div/button/span[contains(text(),'Save as Draft')]"
    GENERATE = "//button[./span/b[contains(text(),'Generate')]]"
    CALCULATE = "//button[./span/b[contains(text(),'Calculate')]]"
    DOWNLOAD = "// div[contains(text(), 'download')]"
    CONTINUE="//button[./span[contains(text(),'Continue')]]"
    RECOMPUTE = "//mat-card/div/button/span[contains(text(),'Recompute')]"
    SUGGESTION_TOOL = "//mat-card/div[./span[text()=' Use our quick suggestion tool ']]/img"
    DOWNLOAD_REPORT = "//button[./span[contains(text(),'Download Report')]]"
    FILTER = "//button[./span[contains(text(),'Apply Filter')]]"
    CHART_BUTTON = "//*[local-name()='g'] / * [local-name()='path' and @class='highcharts-button-symbol']"
    CHART_DROPDOWN = "//li[contains(text(),'{}')]"
    CLICK_CONTINUE = "//button[@type='submit']"
    FILTER_ICON = "//div/span/i[contains(@class,'fa-sliders')]"
    APPLY_FILTER = "//app-filter-component//span[contains(text(),'Apply Filter')]"
    SELECT_FILTER = "//span[contains(text(), '{}')]"
    RESET_FILTER = "//span[contains(text(),'Reset')]"
    UPLOAD_INPUT = "//input[@id ='grade_csv']"
    UPLOAD = "//div[contains(@class,'upload_container')]/div[contains(@class,'upload_text1 font_mulish_regular font_color')][1]"

    VALIDATION_ERROR = {
        "keys": ("test_name",),
        "sleep": 0
    }
    SUBMIT_SLEEP = 1
    SUBMIT_TIMEOUT = 60

    def __init__(self, driver):
        self.driver = driver
        self.driver.wait_for_disappear(self.LOADER, timeout=90)
        self.driver.click("html")
        self.driver.scroll_top()

    def _edit_control(self, definition, **kwargs):
        entry = self.CONTENT + self.FORM_FIX + definition.get("entry_xpath", self.ENTRY).format(definition["label"])
        value = kwargs[definition["key"]]

        if definition["type"] == "input":
            if definition["key"] == "value":
                Input(self.driver, self.CONTENT + self.FORM_FIX+"/div/div").input(value)
            else:
                Input(self.driver, entry).input(value)
                if definition["key"] == "test_name":
                        self.driver.click("html")
                        self.driver.wait_for_disappear(self.LOADER, timeout=120)
                if definition["key"] in self.VALIDATION_ERROR["keys"]:
                    if self.VALIDATION_ERROR.get("sleep"):
                        time.sleep(self.VALIDATION_ERROR.get("sleep"))
                    error_messages = self._find_input_error_messages(entry)
                    if error_messages is not None:
                        raise ValidationException(definition['key'], error_messages)

        elif definition["type"] == "area":
            TextArea(self.driver, entry).input(value)

        elif definition["type"] == "select":
            DropDown(self.driver, entry).select_by_value(value)

        elif definition["type"] == "multi_select":
            MultiSelectDropDown(self.driver, entry).select_by_value(value)

        elif definition["type"] == "checkbox":
            if value == "Select All":
                entry = self.CONTENT + self.FORM_FIX + self.TABLE_HEAD
                CheckBoxList(self.driver, entry).input()
            else:
                if definition["key"] == "confidence_level" or\
                        definition["key"] == "margin_of_error" or\
                        definition["key"] == "number_of_test_store":
                    entry = self.CONTENT + self.CHECKBOX.format(definition["label"])
                    CheckBox(self.driver, entry).input(value)
                else:
                    for item in range(value):
                        num = item + 1
                        entry = self.CONTENT + self.FORM_FIX + self.TABLE + "[" + str(num) + "]/td"
                        CheckBoxList(self.driver, entry).input()

            self.driver.wait_for_disappear(self.LOADER, timeout=120)

        elif definition["type"] == "radio":
            if definition["key"] == "features":
                Radio(self.driver, self.CONTENT).input(value)
            elif definition["key"] == "comparison":
                if self.driver.is_visible(self.CONTENT+"/div"):
                    try:
                        RadioOption(self.driver, self.CONTENT+"/div").input(value)
                    except:
                        self.driver.click("html")
                        self.driver.scroll_down()
                        RadioOption(self.driver, self.CONTENT + "/div").input(value)
            elif definition["key"] == "margin_of_error" or definition["key"] == "no_of_test_store":
                Radio(self.driver, self.CONTENT + self.FORM_FIX).input(value)
            else:
                if self.driver.is_visible(entry):
                    Radio(self.driver, entry).input(value)
                else:
                    self.driver.click("html")
                    self.driver.scroll_down()
                    if len(self.driver.find_all(entry)) == 0:
                        raise Exception(definition["label"] + " Not Found")
                    else:
                        Radio(self.driver, entry).input(value)


        elif definition["type"] == "date":
            DatePicker(self.driver, entry).input(value)

        elif definition["type"] == "download":
            if value is True:
                if not (self.driver.is_visible(self.DOWNLOAD)):
                    try:
                        self.driver.scroll_into_view(self.DOWNLOAD)
                    except:
                        self.driver.click("html")
                        self.driver.scroll_down()
                self.driver.click(self.DOWNLOAD)
                self.driver.wait_for_disappear(self.LOADER, timeout=180)

        elif definition["type"] == "upload_file":
            ele=self.driver.find_element_by_xpath(self.UPLOAD_INPUT)
            ele.send_keys(value)
            self.driver.wait_for_disappear(self.LOADER, timeout=250)
            try:
                self.driver.find(self.UPLOAD)
            except:
                self.driver.click("html")
                self.driver.scroll_down()
            message = (self.driver.find(self.UPLOAD)).text
            if self.UPLOAD_MESSAGE not in message:
                raise Exception(message)

        elif definition["type"] == "search":
            Table(self.driver).search(value)
        else:
            raise NotImplementedError

        self.driver.wait_for_disappear(self.LOADER, timeout=120)


    def default(self, continue_=False, submit_=True, generate=False, save=False, calculate=False, recompute= False,
                ok=False, download_report=False, filter_=False, **kwargs):
        for definition in self.fields:
            if definition["key"] not in kwargs or kwargs[definition["key"]] is None:
                continue
            self._edit_control(definition, **kwargs)

        if generate is True:
            try:
                self.driver.scroll_into_view(self.GENERATE)
            except:
                self.driver.wait_for_disappear(self.LOADER, timeout=90)
                self.driver.click("html")
                self.driver.scroll_down(self.GENERATE)
            self.driver.click(self.GENERATE)
            self.driver.wait_for_disappear(self.LOADER, timeout=300)
            if ok is True:
                AbstractDialog(self.driver).ok()

        if calculate is True:
            try:
                self.driver.click(self.CALCULATE)
            except:
                self.driver.click("html")
                self.driver.scroll_down()
                self.driver.click(self.CALCULATE)

        if recompute is True:
            self.driver.click(self.RECOMPUTE)
            ui.AbstractDialog(self.driver).cbu_level(value='0')
        if filter_ is True:
            val = self.driver.find(self.FILTER)
            val1 = val.get_property("disabled")
            if val1 is True:
                raise ElementNotVisibleException("Filter is disabled")
            else:
                self.driver.click(self.FILTER)

        self.driver.wait_for_disappear(self.LOADER, timeout=240)
        if save is True:
            self.driver.find(self.SAVE_AS_DRAFT)
            self.driver.click(self.SAVE_AS_DRAFT)
            self.driver.wait_for_disappear(self.LOADER, timeout=180)
            return
        if download_report is True:
            self.driver.click(self.DOWNLOAD_REPORT)
        elif submit_ is True:
            time.sleep(self.SUBMIT_SLEEP)
            try:
                self.submit()
            except TAEditFormException:
                self.close()
                raise
        if continue_ is True:
            self.driver.click(self.CONTINUE)

        self.driver.wait_for_disappear(self.LOADER, timeout=200)
        return self

    def _find_input_error_messages(self, input_locator: str):
        try:
            el_errors = self.driver.find_all(
                input_locator + "/div", timeout=0
            )
            if len(el_errors) == 0:
                return None

            return [el_error.get_attribute("innerText") for el_error in el_errors]
        except:
            return None

    def _handle_dialog_error(self):
        try:
            error_text = None
            error_text = self.driver.text(self.MESSAGE_CONTAINER, timeout=2)
        except (GenericException, NoSuchElementException):
            pass
        if error_text is not None:
            raise TAEditFormException(error_text)
        for definition in self.fields:
            entry = self.CONTENT + self.FORM_FIX + definition.get("entry_xpath", self.ENTRY).format(definition["label"])
            error_messages = self._find_input_error_messages(entry)
            if error_messages:
                raise ValidationException(definition['key'], error_messages)

    def submit(self):
        def method():
            self.driver.click(self.BUTTON)
            self.driver.wait_for_disappear(self.LOADER, timeout=90)
            time.sleep(self.SUBMIT_SLEEP)
            self.driver.wait_for_disappear(self.LOADER, timeout=200)
        self.driver.wait_until(method, timeout=self.SUBMIT_TIMEOUT)

        return self

    def click_tool(self):
        self.driver.find(self.SUGGESTION_TOOL)
        self.driver.click(self.SUGGESTION_TOOL)

    def stat(self):
        res = {}
        for key, field_value in self.fields.items():

            locator_base = self.BASE + self.FORM + field_value.get("entry_xpath", self.ENTRY).format(
                field_value["label"])
            entry = self.driver.find_all(locator_base)
            if len(entry) == 0:
                raise ControlNotFoundException(key)

            if field_value["type"] == "text":
                try:
                    res[key] = self.driver.text(locator_base + field_value.get("text_xpath", self.TEXT), timeout=2)
                except ElementNotVisibleException:
                    res[key] = None
                if res[key] == "":
                    res[key] = None
            elif field_value["type"] == "area":
                res[key] = self.driver.find(locator_base + field_value.get("area_xpath", self.AREA)).get_attribute(
                    "value")
                if res[key] == "":
                    res[key] = None

            elif field_value["type"] == "boolean":
                res[key] = "ice-yes" in self.driver.find(
                    locator_base + field_value.get("boolean_xpath", self.BOOLEAN)).get_attribute("class")

            elif field_value["type"] == "list":
                temp_res = []
                for item in self.driver.find_all(locator_base + field_value.get("list_xpath", self.LIST_ITEM)):
                    temp_res.append(item.text)
                res[key] = tuple(temp_res)

            else:
                raise GenericException({"message": f"Invalid type {field_value['type']}"})

        additional = self._stat_additional()

        return _.defaults(res, additional)

    def _stat_additional(self):
        return {}

    def click_header_btn(self, btn_text='Edit'):
        locator = self.BASE + self.HEADER + self.HEADER_BTN.format(btn_text)
        try:
            self.driver.click(locator)
        except:
            self.driver.scroll_into_view(locator)
            self.driver.click(locator)

    def click_edit(self):
        self.click_header_btn()

    def get_values(self):
        Auto_pop_values = {}
        for definition in self.fields:
            entry = self.CONTENT + self.FORM_FIX + self.ENTRY.format(definition["label"])
            if definition["type"] == "input":
                keys = definition["label"]
                if definition["label"] == "Cost impact for one store":
                    self.driver.scroll_top()
                else:
                    time.sleep(2)
                    self.driver.scroll_down()
                values = Input(self.driver, entry).get_value()
                Auto_pop_values.update({keys: values})
        return Auto_pop_values


    def percentage_filter(self, filter_, option=None):
        self.driver.click(self.FILTER_ICON)
        self.driver.click(self.SELECT_FILTER.format(filter_))
        filter_options = CheckBoxSelect(self.driver).select_option(option)
        self.driver.wait_for_disappear(self.LOADER, timeout=90)
        self.driver.click(self.APPLY_FILTER)
        self.driver.wait_for_disappear(self.LOADER, timeout=120)
        return filter_options

class EditEnterTestDetails(Edit):

    fields = [
        {
            "key": "test_name",
            "label": "Enter Test Name",
            "type": "input"
        }, {
            "key": "type_of_test",
            "label": "Select Type of Test",
            "type": "select"
        }, {
            "key": "target_variables",
            "label": "Target Variable ",
            "type": "select"
        }, {
            "key": "brief_description",
            "label": "Enter Brief Description",
            "type": "input"
        }, {
            "key": "additional_details",
            "label": "Enter Additional Details",
            "type": "area"
        }, {
            "key": "pre_test_window",
            "label": "Pre-Test Window",
            "type": "date"
        }, {
            "key": "post_test_window",
            "label": "Post-Test Window",
            "type": "date"
        }
    ]


class EditApplicabilityCriteria(Edit):
    FORM_FIX = "/div"
    ENTRY = '//div[./label[contains(text(),"{}")]]'
    DOWNLOAD = "//div[contains(@class,'download_template')]"
    UPLOAD_MESSAGE = "The Stores are Uploaded Successfully"
    UPLOAD = "//div[@class='upload_container mt-2']/div[contains(@class,'upload_text1')]"



    fields = [
        {
            "key": "customer_group",
            "label": "Select Customer Group",
            "type": "multi_select"
        }, {
            "key": "territory",
            "label": "Select Territory",
            "type": "multi_select"
        }, {
            "key": "customer_chain",
            "label": "Select Customer Chain",
            "type": "multi_select"
        }, {
            "key": "sub_channel",
            "label": "Select Sub Channel",
            "type": "multi_select"
        }, {
            "key": "cbu_level_1",
            "label": "Select CBU Level 1",
            "type": "multi_select"
        }, {
            "key": "pack_format",
            "label": "Select Pack Format",
            "type": "multi_select"
        }, {
            "key": "timeframe",
            "label": "Select timeframe to estimate Annual RSV",
            "type": "date"
        }, {
            "key": "cost_impact_for_one_store",
            "label": "Cost impact for one store",
            "type": "input"
        }, {
            "key": "download_template",
            "label": "Click here to download the template",
            "type": "download"
        },  {
            "key": "upload_file",
            "label": "Upload File",
            "type": "upload_file"
        }, {
            "key": "store_feature_1",
            "label": "Store Feature - 1",
            "type": "radio"
        }, {
            "key": "store_feature_2",
            "label": "Store Feature - 2",
            "type": "radio"
        }, {
            "key": "cost_impact",
            "label": "Estimated Cost Impact (£)",
            "type": "input"
        }, {
            "key": "annual_rsv",
            "label": "Annual RSV (£ in million)",
            "type": "input"
        }, {
            "key": "breakeven_lift",
            "label": "Breakeven Lift (%)",
            "type": "input"
        }
    ]


class EditApplicabilityCriteriaRussia(Edit):
    FORM_FIX = "/div"
    ENTRY = "//div[./label[contains(text(),'{}')]]"

    fields = [
        {
            "key": "channel_name",
            "label": "Select Channel Name",
            "type": "multi_select"
        }, {
            "key": "outlet_type",
            "label": "Select Outlet Type",
            "type": "multi_select"
        }, {
            "key": "chain_tier",
            "label": "Select Chain Tier",
            "type": "multi_select"
        }, {
            "key": "chain_name",
            "label": "Select Chain Name",
            "type": "multi_select"
        }, {
            "key": "segment",
            "label": "Select Segment",
            "type": "multi_select"
        }, {
            "key": "region",
            "label": "Select Region",
            "type": "multi_select"
        }, {
            "key": "distributor",
            "label": "Select Distributor",
            "type": "multi_select"
        }, {
            "key": "product_type",
            "label": "Select Product Type",
            "type": "multi_select"
        }, {
            "key": "timeframe",
            "label": "Select timeframe to estimate Annual LSV",
            "type": "date"
        }, {
            "key": "cost_impact_for_one_store",
            "label": "Cost impact for one store (₽)",
            "type": "input"
        }, {
            "key": "download_template",
            "label": "Click here to download the template",
            "type": "download"
        },  {
            "key": "upload_file",
            "label": "Upload File",
            "type": "upload_file"
        },  {
            "key": "cost_impact",
            "label": "Estimated Cost Impact (₽)",
            "type": "input"
        }, {
            "key": "annual_rsv",
            "label": "Annual LSV (₽ )",
            "type": "input"
        }, {
            "key": "breakeven_lift",
            "label": "Breakeven Lift (%)",
            "type": "input"
        }
    ]


class EditSelectTestStoreConfigDetails(Edit):
    FORM_FIX = ""
    ENTRY = "/div[./span[text()='{}']]/div"
    CHECKBOX = "//div[./label[contains(text(),'{}')]]"

    UPLOAD_MESSAGE = "The number of recommended test stores"


    fields = [
        {
            "key": "test_store",
            "label": "How would you like to select test stores?",
            "type": "radio"
        },
        {
            "key": "confidence_level",
            "label": "Confidence Level",
            "type": "checkbox"
        },
        {
            "key": "margin_of_error",
            "label": "Margin of Error",
            "type": "checkbox"
        },
        {
            "key": "number_of_test_store",
            "label": "Number of Test store",
            "type": "checkbox"
        },
        {
            "key": "upload_file",
            "label": "Upload File",
            "type": "upload_file"
        },
        {
            "key": "download_template",
            "label": "Click here to download the template",
            "type": "download"}
       ]


class EditSuggestionToolTestStore(Edit):
    FORM_FIX = "/div"

    fields = [
         {
            "key": "margin_of_error",
            "label": "Margin of error %",
            "type": "radio"
         },
         {
            "key": "no_of_test_store",
            "label": "No of test stores",
            "type": "radio"
         },
         {
            "key": "value",
            "label": "value",
            "type": "input"
         }
       ]


class EditSelectTestStore(Edit):
    FORM_FIX = ""
    TABLE = "/div/app-common-table/table/tbody/tr"
    TABLE_HEAD = "/div/app-common-table/table/thead/tr/th"


    fields = [
         {
            "key": "stores",
            "label": "Selected number of stores",
            "type": "checkbox"
         }, {
            "key": "search",
            "label": "search",
            "type": "search"
         },

       ]


class EditTestStoreCorrelation(Edit):
    fields = []


class EditControlStoreMapping(Edit):
    FORM_FIX = ""
    GENERATE = "//button[./span[contains(text(),'Generate')]]"
    UPLOAD_MESSAGE = "of them are valid"
    fields = [
         {
            "key": "features",
            "label": "Selected features to Map control and test stores",
            "type": "radio"
         }, {
            "key": "no_of_stores",
            "label": "No. of Control Store per test store",
            "type": "input"
         },  {
            "key": "download_template",
            "label": "Click here to download the template",
            "type": "download"
         }, {
            "key": "upload_file",
            "label": "Upload File",
            "type": "upload_file"
         },
       ]


class EditGenerateControlStores(Edit):
    BUTTON = "//mat-card/div/button/span[contains(text(),'Initiate test')]"
    fields = []


class EditTestDetailsToAnalyse(Edit):
    FORM_FIX = "/div[2]"
    BUTTON = "//mat-card/div/button/span[contains(text(),'Analyse')]"

    fields = [
        {
            "key": "test_name",
            "label": "Select Test Name",
            "type": "select"
        }, {
            "key": "type_of_test",
            "label": "Description",
            "type": "input"
        }
    ]


class EditImpactSummery(Edit):
    CONTENT = "//mat-card"
    FORM_FIX = "/"
    ENTRY = "/div[./label[contains(text(),'{}')]]"

    fields = [
        {
            "key": "cbu_level_1",
            "label": "Select CBU Level 1",
            "type": "multi_select"
        },
        {
            "key": "pack_format",
            "label": "Select Pack Format",
            "type": "multi_select"
        }
    ]


class EditPercentageChange(Edit):

    fields = [
        {
            "key": "to_analyze",
            "label": "I would like to analyze",
            "type": "select",
        }, {
            "key": "to_see",
            "label": "What would you like to see?",
            "type": "radio"
        }, {
            "key": "comparison",
            "label": "What would you like to see?",
            "type": "radio"
         }
    ]


class EditTestMeasurementResults(Edit):

    fields = [
        {
            "key": "to_analyze",
            "label": "I would like to analyze",
            "type": "select",
        }
    ]


class EditTestResultGrid(Edit):

    fields = [
        {
            "key": "metric",
            "label": "Choose metric",
            "type": "select",
        },
        {
            "key": "variables",
            "label": "Choose variable to show on grid",
            "type": "multi_select",
        },
        {
            "key": "shading_metrics",
            "label": "Choose shading metric",
            "type": "select",
        }
    ]
