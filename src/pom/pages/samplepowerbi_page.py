import time
import allure
import pandas as pd
import datacompy
from selenium.webdriver.common.by import By
from ....src.pom.pages.base_page import BasePageElement
from selenium.webdriver.common.action_chains import ActionChains
from ....utilities.dfUtil import df_compare_with_equal_vals, df_compare_with_equal_valscheck
from ....utilities.CustomLogging import getLogger

log = getLogger()


class SummaryReportPage(BasePageElement):
    """Base page class that is initialized on every page object class."""

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.action = ActionChains(self.driver)

    resetFilter = "//*[text()='Reset']"
    yearDropDown = "(//*[local-name()='div' and @class='slicer-restatement'])[1]"
    commodityGroup = "(//*[local-name()='div' and @class='slicer-restatement'])[2]"
    commodityFilter = "(//*[local-name()='div' and @class='slicer-restatement'])[3]"
    sectorFilter = "(//*[local-name()='div' and @class='slicer-restatement'])[4]"
    countryFilter = "(//*[local-name()='div' and @class='slicer-restatement'])[5]"
    countryRegionFilter = "(//*[local-name()='div' and @class='slicer-restatement'])[6]"
    totalSpendBySectorCol = "(//*[local-name()='g' and @class='x axis hideLinesOnAxis setFocusRing'])[1]//*[name()='g' and @class='tick']"
    SensitivityBySpend = "(//*[local-name()='g' and @class='x axis hideLinesOnAxis setFocusRing'])[3]//*[name()='g' and @class='tick']"
    SpendByPriorYear = "(//*[local-name()='g' and @class='x axis hideLinesOnAxis setFocusRing'])[2]//*[name()='g' and @class='tick']"
    columnExecutive = "(//*[local-name()='div' and @class='scrollable-cells-container '])[1]//*[name()='div' and @class='pivotTableCellWrap cell-interactive tablixAlignCenter main-cell ']"
    commodityExecutive = "//*[local-name()='div' and @class='pivotTableCellWrap cell-interactive main-cell ']"
    newXpath = "(//*[local-name()='g' and @class='x axis hideLinesOnAxis setFocusRing'])[1]//*[name()='g' and @class='tick'][1]"

    def reset_Filter_Report(self):
        time.sleep(45)
        log.info("Reset Filter")
        with allure.step("Reset Filter"):
            ele = self.find_element_by_locator(By.XPATH, "//*[text()='Reset']")
            self.action.click(ele).perform()

    def filter_Select_Report(self, Val, Val1, Val2, Val3, Val4, Val5):
        time.sleep(5)
        log.info("Filter the power bi based on filter options")
        with allure.step("Filter the power bi based on filter options"):
            self.click_by_locator(By.XPATH, self.yearDropDown)
            self.find_element_by_locator(By.XPATH, "//span[text()='" + Val + "']").click()
            self.click_by_locator(By.XPATH, self.yearDropDown)
            time.sleep(2)
            self.click_by_locator(By.XPATH, self.commodityGroup)
            self.find_element_by_locator(By.XPATH, "//span[text()='" + Val1 + "']").click()
            self.click_by_locator(By.XPATH, self.commodityGroup)
            time.sleep(2)
            self.click_by_locator(By.XPATH, self.commodityFilter)
            self.find_element_by_locator(By.XPATH, "//span[text()='" + Val2 + "']").click()
            self.click_by_locator(By.XPATH, self.commodityFilter)
            time.sleep(2)
            self.click_by_locator(By.XPATH, self.sectorFilter)
            self.find_element_by_locator(By.XPATH, "//span[text()='" + Val3 + "']").click()
            self.click_by_locator(By.XPATH, self.sectorFilter)
            time.sleep(2)
            self.click_by_locator(By.XPATH, self.countryFilter)
            self.find_element_by_locator(By.XPATH, "//span[text()='" + Val4 + "']").click()
            self.click_by_locator(By.XPATH, self.countryFilter)
            time.sleep(2)
            self.click_by_locator(By.XPATH, self.countryRegionFilter)
            self.find_element_by_locator(By.XPATH, "//span[text()='" + Val5 + "']").click()
            self.click_by_locator(By.XPATH, self.countryRegionFilter)

    def validate_Total_Spend_By_Sector(self):
        log.info("Validate Total spend by sector bar graph against SQL")
        with allure.step("Validate Total spend by sector bar graph against SQL"):

            Col = len(self.find_elements_by_locator(By.XPATH, self.totalSpendBySectorCol))
            print(Col)
            pos = 0

            print("Entering the dataframe")
            df = pd.DataFrame(columns=['Sector', 'Spend'])

            for ol in range(1, Col + 1):
                data = []
                h2 = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='g' and @class='x axis hideLinesOnAxis setFocusRing'])[1]//*[name()='g' and @class='tick'][" + str(
                        ol) + "]").text
                div_2 = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='svg' and @class='mainGraphicsContext setFocusRing'])[1]//*[name()='rect' and @class='column setFocusRing'][" + str(
                        ol) + "]").get_attribute("aria-label")
                data.append(h2)
                data.append(int(div_2))
                df.loc[pos] = data
                pos += 1

            print(df)

            dfcheck = self.connectTosqlTest("select * from dbo.[Total_Spend_By_Sector]")
            print(dfcheck)

            base_df = df
            compare_df = dfcheck

            comparison = datacompy.Compare(base_df, compare_df, join_columns='Sector', abs_tol=0, rel_tol=0)
            print(comparison.matches())
            if comparison.matches()==True:
                log.info("The dataframe matches with the other")
                assert True
            else:
                log.info("The dataframe doesnt match with the other")
                print("The dataframe doesnt match with the other")
                assert False

    def validate_Total_Spend_By_SectorPriorYear(self):
        log.info("validate_Total_Spend_By_SectorPriorYear bar graph against SQL")
        with allure.step("validate_Total_Spend_By_SectorPriorYear bar graph against SQL"):

            Col = len(self.find_elements_by_locator(By.XPATH, self.SpendByPriorYear))
            print(Col)
            pos = 0

            print("Entering the dataframe")
            dfprior = pd.DataFrame(columns=['Sector', 'SpendPriorYear'])

            for ol in range(1, Col + 1):
                data = []
                h2 = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='g' and @class='x axis hideLinesOnAxis setFocusRing'])[2]//*[name()='g' and @class='tick'][" + str(
                        ol) + "]").text
                div_2 = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='svg' and @class='mainGraphicsContext setFocusRing'])[2]//*[name()='rect' and @class='column setFocusRing'][" + str(
                        ol) + "]").get_attribute('aria-label')
                data.append(h2)
                data.append(int(div_2))
                dfprior.loc[pos] = data
                pos += 1

            print(dfprior)
            dfcheck2 = self.connectTosqlTest("select * from dbo.Spend_Sector_With_Prior_Year")
            base_df = dfprior
            compare_df = dfcheck2
            comparison = datacompy.Compare(base_df, compare_df, join_columns='Sector', abs_tol=0, rel_tol=0)
            print(comparison.matches())
            if comparison.matches()==True:
                log.info("The dataframe matches with the other")
                assert True
            else:
                log.info("The dataframe doesnt match with the other")
                print("The dataframe doesnt match with the other")
                assert False


    def validate_Total_Sensitivity_By_sector(self):
        log.info("validate_Total_Sensitivity_By_sector bar graph against SQL")
        with allure.step("validate_Total_Sensitivity_By_sector bar graph against SQL"):

            Col = len(self.find_elements_by_locator(By.XPATH, self.SensitivityBySpend))
            print(Col)
            pos = 0

            print("Entering the dataframe")
            dfsensitivity = pd.DataFrame(columns=['Sector', 'Sensitivity'])

            for ol in range(1, Col + 1):
                data = []
                h2 = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='g' and @class='x axis hideLinesOnAxis setFocusRing'])[3]//*[name()='g' and @class='tick'][" + str(
                        ol) + "]").text
                div_2 = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='svg' and @class='mainGraphicsContext setFocusRing'])[3]//*[name()='rect' and @class='column setFocusRing'][" + str(
                        ol) + "]").get_attribute('aria-label')
                data.append(h2)
                data.append(int(div_2))
                dfsensitivity.loc[pos] = data
                pos += 1

            print(dfsensitivity)
            dfcheck3 = self.connectTosqlTest("select * from dbo.Sensitivity_By_Sector")
            base_df = dfsensitivity
            compare_df = dfcheck3
            comparison = datacompy.Compare(base_df, compare_df, join_columns='Sector', abs_tol=0, rel_tol=0)
            print(comparison.matches())

            if comparison.matches()==True:
                log.info("The dataframe matches with the other")
                assert True

            else:
                log.info("The dataframe doesnt match with the other")
                print("The dataframe doesnt match with the other")
                assert False
            print(comparison.report())
            print(comparison.all_columns_match())
            print(comparison.all_rows_overlap())

    def validate_executive_summary(self):
        log.info("Validate executive summary table data against sql")
        with allure.step(""):
            Col = len(self.find_elements_by_locator(By.XPATH, self.columnExecutive))
            print(Col)
            pos = 0
            data = []
            for ol in range(1, Col + 1):
                h2 = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='div' and @class='scrollable-cells-container '])[1]//*[name()='div' and @class='pivotTableCellWrap cell-interactive tablixAlignCenter main-cell '][" + str(
                        ol) + "]").text
                data.append(h2)

                pos += 1

            print(data)

            dfExecutive = pd.DataFrame(columns=data)
            Col1 = len(self.find_elements_by_locator(By.XPATH, self.commodityExecutive))
            print(Col1)
            pos = 0

            for ol in range(1, Col + 1):
                data = []

                Commodity = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='div' and @class='pivotTableCellWrap cell-interactive main-cell '])[" + str(
                        ol) + "]").text

                FY_Spend = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='div' and @class='mid-viewport']//*[name()='div' and @class='pivotTableCellWrap cell-interactive tablixAlignRight main-cell ' and @column-index=1])[" + str(
                        ol) + "]").text
                Spend_percent = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='div' and @class='mid-viewport']//*[name()='div' and @class='pivotTableCellWrap cell-interactive tablixAlignRight main-cell ' and @column-index=2])[" + str(
                        ol) + "]").text
                Q1 = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='div' and @class='mid-viewport']//*[name()='div' and @class='pivotTableCellWrap cell-interactive tablixAlignRight main-cell ' and @column-index=3])[" + str(
                        ol) + "]").text
                Q2 = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='div' and @class='mid-viewport']//*[name()='div' and @class='pivotTableCellWrap cell-interactive tablixAlignRight main-cell ' and @column-index=4])[" + str(
                        ol) + "]").text
                Q3 = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='div' and @class='mid-viewport']//*[name()='div' and @class='pivotTableCellWrap cell-interactive tablixAlignRight main-cell ' and @column-index=5])[" + str(
                        ol) + "]").text
                Q4 = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='div' and @class='mid-viewport']//*[name()='div' and @class='pivotTableCellWrap cell-interactive tablixAlignRight main-cell ' and @column-index=6])[" + str(
                        ol) + "]").text
                FY_Volume_Coverage = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='div' and @class='mid-viewport']//*[name()='div' and @class='pivotTableCellWrap cell-interactive tablixAlignRight main-cell ' and @column-index=7])[" + str(
                        ol) + "]").text
                Sensitivity_On_Open_Positions = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='div' and @class='mid-viewport']//*[name()='div' and @class='pivotTableCellWrap cell-interactive tablixAlignRight main-cell ' and @column-index=8])[" + str(
                        ol) + "]").text
                Open_Spend = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='div' and @class='mid-viewport']//*[name()='div' and @class='pivotTableCellWrap cell-interactive tablixAlignRight main-cell ' and @column-index=9])[" + str(
                        ol) + "]").text
                Planned_Spend = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='div' and @class='mid-viewport']//*[name()='div' and @class='pivotTableCellWrap cell-interactive tablixAlignRight main-cell ' and @column-index=10])[" + str(
                        ol) + "]").text
                Covered_Price = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='div' and @class='mid-viewport']//*[name()='div' and @class='pivotTableCellWrap cell-interactive tablixAlignRight main-cell ' and @column-index=11])[" + str(
                        ol) + "]").text
                Guidance_Price = self.find_element_by_locator(By.XPATH,
                    "(//*[local-name()='div' and @class='mid-viewport']//*[name()='div' and @class='pivotTableCellWrap cell-interactive tablixAlignRight main-cell ' and @column-index=12])[" + str(
                        ol) + "]").text

                data.append(Commodity)
                data.append(FY_Spend)
                data.append(Spend_percent)
                data.append(Q1)
                data.append(Q2)
                data.append(Q3)
                data.append(Q4)
                data.append(FY_Volume_Coverage)
                data.append(Sensitivity_On_Open_Positions)
                data.append(Open_Spend)
                data.append(Planned_Spend)
                data.append(Covered_Price)
                data.append(Guidance_Price)
                dfExecutive.loc[pos] = data
                pos += 1

            print(dfExecutive)
