from .create_new_test import CreateNewTest
from .analyse_test_impact import AnalyseTestImpact
from ..ui.side_menu import SideMenu, SideMenuOption
from ..ui.details import Top, History, Getting_started
from .. import ui


class Dashboard:

    def __init__(self, driver):
        self.driver = driver

    def left_menu(self):
        return SideMenu(self.driver).list_category()

    def mars_wrigley(self, switch=True):
        return SideMenu(self.driver).switch_collapse(switch)

    def go(self, target):
        if target == "dashboard":
            SideMenu(self.driver).select_option(SideMenuOption.DASHBOARD)
            return Dashboard(self.driver)
        if target == "create new test":
            SideMenu(self.driver).select_option(SideMenuOption.CREATE_NEW_TEST)
            return CreateNewTest(self.driver)
        if target == "analyse test impact":
            SideMenu(self.driver).select_option(SideMenuOption.ANALYSE_TEST_IMPACT)
            return AnalyseTestImpact(self.driver)

        raise NotImplementedError

    def country_dropdown(self):
        return SideMenu(self.driver).county_dropdown()

    def admin_message(self):
        return Top(self.driver).admin_message()

    def summary(self):
        return Top(self.driver).summary()

    def impact(self):
        return Top(self.driver).impact()

    def search(self, query):
        ui.Table(self.driver).search(query)

    def dashboard_search(self, query):
        ui.Table(self.driver).dashboard_search(query)
        return CreateNewTest(self.driver)

    def delete(self, id_):
        ui.Table(self.driver).open_menu(id_=id_)
        ui.Menu(self.driver).select("Delete")
        ui.AbstractDialog(self.driver).primary()
        ui.Alert(self.driver).success("deleted successfully")

    def edit(self, id_):
        ui.Table(self.driver).open_menu(id_=id_)
        ui.Menu(self.driver).select("Edit")
        return CreateNewTest(self.driver)

    def history(self, id_):
        ui.Table(self.driver).open_menu(id_=id_)
        ui.Menu(self.driver).select("History")
        return History(self.driver).history()

    def analyse_impact(self, id_):
        ui.Table(self.driver).open_menu(id_=id_)
        ui.Menu(self.driver).select("Analyse Impact")
        return AnalyseTestImpact(self.driver)

    def dashboard_table_configure_grid(self, query):
        ui.TableAllTests(self.driver).configure_grid(query)

    def table_header(self, column_name):
        ui.Table(self.driver).table_scroll()
        return ui.Table(self.driver).click_table_header(column_name)

    def items_per_page(self, item):
        ui.Table(self.driver).item_per_page(item)

    def notification(self):
        Top(self.driver).click_notification()

    def mark_as_all_read(self):
        Top(self.driver).mark_as_all_read()

    def how_to_run(self):
        return Getting_started(self.driver).how_to_run()

    def what_to_know(self):
        return Getting_started(self.driver).what_to_know()

    def ideal_duration(self):
        return Getting_started(self.driver).ideal_duration()

    def initiated_test(self):
        return Getting_started(self.driver).initiated_test()

    def action(self, name):
        ui.Table(self.driver).open_menu(id_=name)
        return ui.Table(self.driver).action()

    def list(self, detail=True):
        return ui.TableAllTests(self.driver).list(detail)

    def filter_(self, filter_, option):
        return ui.Table(self.driver).filter_(filter_, option)




