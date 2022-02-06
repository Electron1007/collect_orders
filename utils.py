import gspread
import re

order_data_range = range(52,59)
order_ranges = {
    "Monday":range(2,12),
    "Tuesday":range(12,22),
    "Wednesday":range(22,32),
    "Thursday":range(32,42),
    "Friday":range(42,52)
    }

class OrderData():
    service_account = gspread.service_account(filename=".config\gspread\service_account.json") # TODO move service account key to another custom folder

    my_sheet = service_account.open("Orders_14-18_feb") 
    wks = my_sheet.worksheet("Відповіді форми (1)")

    all_values =wks.get_all_values()

    def order_data(self, n):
        res = {self.all_values[0][1]:self.all_values[n][1]}  # електронна адреса

        for i in order_data_range:
            if  self.all_values[n][i]:
                res[self.all_values[0][i]] = self.all_values[n][i]

        return res
    
    def get_order_for(self, day, n):
        res=[]
        for i in order_ranges[day]:
            if  self.all_values[n][i]:
                name = re.search(r'(?<=\[).*(?=\()', self.all_values[0][i]).group(0)
                price= re.search(r'\d+(?=(\ ₴|\₴))',  self.all_values[0][i]).group(0)
                quantity = self.all_values[n][i]
                res.append([name, price, quantity])

        return res

    def orders_quantity(self):
        return len(self.wks.get_values(f"A1:A{self.wks.row_count}")) - 1



class CreatePDF:
    pass
