

class Map:
    LOADER = "//div[@class='ngx-overlay loading-foreground']"
    MAP_ICON = "//button[@id='mat-button-toggle-2-button']"
    MAP_POINTS = "//agm-map//div[@role='button']/img"

    def __init__(self, driver):
        self.driver = driver

    def click_map(self):
        self.driver.wait_for_disappear(self.LOADER, timeout=120)
        self.driver.click(self.MAP_ICON)
        if self.driver.is_visible(self.MAP_POINTS):
            location_points = self.driver.find_all(self.MAP_POINTS)
            return len(location_points)