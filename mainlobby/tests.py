from seleniumbase import BaseCase
class MyTestClass(BaseCase):
    def test_swag_labs(self):
        self.open("https://www.saucedemo.com")
        print('done')

test = MyTestClass()
test.test_swag_labs()