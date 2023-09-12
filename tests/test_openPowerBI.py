import allure
import pytest
from ..tests.Testbase import BaseTest
from ..tests.settings import emailID, encryptedPasscode,testdataPath
from ..tests.testData import get_data_from_excel
from ..utilities.CustomLogging import getLogger
from ..utilities.encryption import decode
log = getLogger()


class TestPowerBIReport(BaseTest):

    @pytest.mark.smoke
    @pytest.mark.parametrize("filter1,filter2,filter3,filter4,filter5,filter6",
                             get_data_from_excel(testdataPath, "Sheet1"))
    @allure.title("Power bi comparison with sql")
    def test_report(self,filter1,filter2,filter3,filter4,filter5,filter6):
        self.OpenPowerBI.power_BI_login(emailID, decode(encryptedPasscode))
        self.summaryReport.reset_Filter_Report()
        self.summaryReport.filter_Select_Report(filter1,filter2,filter3,filter4,filter5,filter6)
        self.summaryReport.reset_Filter_Report()
        #Need db set up in machine to run the below functions
        #self.summaryReport.validate_Total_Spend_By_Sector()
        #self.summaryReport.validate_Total_Sensitivity_By_sector()
        #self.summaryReport.validate_Total_Spend_By_SectorPriorYear()
        #self.summaryReport.validate_executive_summary()
