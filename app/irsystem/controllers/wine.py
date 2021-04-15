# this module is deprecated

class Wine:
  def __init__(self, country, description, designation, points, price, province, region_1, region_2, title, variety, winery):
    self.country = country
    self.description = description
    self.designation = designation
    self.points = points
    self.price = price
    self.province = province
    self.region_1 = region_1
    self.region_2 = region_2
    self.title = title
    self.variety = variety
    self.winery = winery

  def get_country(self):
    return self.country

  def get_description(self):
    return self.description

  def get_designation(self):
    return self.designation

  def get_points(self):
    return self.points

  def get_price(self):
    return self.price

  def get_province(self):
    return self.province

  def get_regions(self):
    return (self.region1, self.region2)

  def get_title(self):
    return self.title

  def get_variety(self):
    return self.variety

  def get_winery(self):
    return self.winery