from .analyse_test_impact import AnalyseTestImpact
from .. import ui



class CreateNewTest(object):
    def __init__(self, driver):
        self.driver = driver

    def enter_test_details(self, **kwargs):
        ui.EditEnterTestDetails(self.driver).default(**kwargs)


    def applicability_criteria(self, **kwargs):
        ui.EditApplicabilityCriteria(self.driver).default(**kwargs)

    def applicability_criteria_russia(self, **kwargs):
        ui.EditApplicabilityCriteriaRussia(self.driver).default(**kwargs)

    def select_test_stores_details(self, **kwargs):
        ui.EditSelectTestStoreConfigDetails(self.driver).default(**kwargs)

    def list(self, detail=True):
        return ui.TableSelectStores(self.driver).list(detail)

    def quick_suggestion_tool(self, **kwargs):
        ui.Edit(self.driver).click_tool()
        ui.EditSuggestionToolTestStore(self.driver).default(**kwargs)

    def select_test_stores(self, **kwargs):
        return ui.EditSelectTestStore(self.driver).default(**kwargs)

    def select_test_stores_map(self):
        return ui.Map(self.driver).click_map()

    def items_per_page(self, item):
        ui.Table(self.driver).item_per_page(item)

    def table_header(self, column_name):
        return ui.Table(self.driver).click_table_header(column_name)

    def select_test_store_search(self,query):
        ui.Table(self.driver).search(query)

    def filter_(self, filter_):
        return ui.Table(self.driver).filter_(filter_)

    def get_values(self):
        return ui.EditApplicabilityCriteria(self.driver).get_values()

    def test_store_correlation(self, **kwargs):
        ui.EditTestStoreCorrelation(self.driver).default(**kwargs)

    def control_store_mapping(self, **kwargs):
        ui.EditControlStoreMapping(self.driver).default(**kwargs)

    def correlation_table_list(self, detail=True):
        return ui.TableStoresCorrelation(self.driver).list(detail)

    def control_table_checkbox(self):
        ui.Table(self.driver).control_table_checkbox()

    def generate_control_stores(self, **kwargs):
        ui.EditGenerateControlStores(self.driver).default(**kwargs)
        return AnalyseTestImpact(self.driver)

    def test_store_configure_grid(self, query):
        ui.TableSelectStores(self.driver).configure_grid(query)

    def control_store_configure_grid(self, query):
        ui.TableControlStores(self.driver).configure_grid(query)

    def search(self, query):
        ui.Table(self.driver).search(query)

    def control_store_list(self, detail=True):
        return ui.TableControlStores(self.driver).list(detail)

    def comparision_summary(self):
        ui.Chart(self.driver).comparison_summary_chart()

    def download_chart(self, index, option):
        ui.Chart(self.driver).download_chart(index, option)


