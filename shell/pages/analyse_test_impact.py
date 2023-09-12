
from .. import ui

class AnalyseTestImpact(object):
    def __init__(self, driver):
        self.driver = driver

    def test_details_to_analyse(self, **kwargs):
        ui.EditTestDetailsToAnalyse(self.driver).default(**kwargs)

    def impact_summery(self, **kwargs):
        ui.EditImpactSummery(self.driver).default(**kwargs)

    def percentage_change(self, **kwargs):
        ui.EditPercentageChange(self.driver).default(**kwargs)

    def test_measurement_results(self, **kwargs):
        ui.EditTestMeasurementResults(self.driver).default(**kwargs)

    def result_grid(self, **kwargs):
        ui.EditTestResultGrid(self.driver).default(**kwargs)

    def download_report(self, **kwargs):
        ui.AbstractDialog(self.driver).download_report(**kwargs)

    def download_chart(self, index, option):
        ui.Chart(self.driver).download_chart(index, option)


    def filter_(self, filter_):
        return ui.Table(self.driver).filter_(filter_)

    def percentage_filter(self, filter_):
        return ui.Edit(self.driver).percentage_filter(filter_)

    def measurement_table_list(self, detail=True):
        return ui.TestMeasurementTable(self.driver).list(detail)

    def test_measurement_search(self, query):
        ui.Table(self.driver).search(query)

    def test_measurement_configure_grid(self, query):
        ui.TestMeasurementTable(self.driver).configure_grid(query)


    def items_per_page(self, item):
        ui.Table(self.driver).item_per_page(item)