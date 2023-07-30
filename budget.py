import math
from itertools import zip_longest


class Category:

  def __init__(self, category_name):
    self.name = category_name
    self.ledger = []

  def __str__(self):
    bill_header = str(self.name).center(30, '*') + "\n"
    ledger = [(item['description'][0:23], format(item['amount'], '.2f'))
              for item in self.ledger]
    print_list = []
    for item in ledger:
      mid_space = len(item[0]) + len(item[1])
      print_list.append(f"{item[0]+' '*(30-mid_space)+item[1]}\n")
    total = f"Total: {self.get_balance()}"
    print_list.insert(0, bill_header)
    print_list.append(total)
    return ''.join(print_list)

  def get_balance(self):
    return sum([item["amount"] for item in self.ledger])

  def check_funds(self, amount):
    if amount > self.get_balance():
      return False
    else:
      return True

  def deposit(self, *args):
    description = args[1] if len(args) > 1 else ""
    entry = {"amount": args[0], "description": description}
    self.ledger.append(entry)

  def withdraw(self, *args):
    description = args[1] if len(args) > 1 else ""
    entry = {"amount": -args[0], "description": description}

    if self.check_funds(args[0]):
      self.ledger.append(entry)
      return True
    else:
      return False

  def transfer(self, amount, category):
    deduct = self.withdraw(amount, f"Transfer to {category.name}")
    if deduct:
      category.deposit(amount, f"Transfer from {self.name}")
      return True
    else:
      return False


def create_spend_chart(categories):
  percent_bar = [
    "  0|", " 10|", " 20|", " 30|", " 40|", " 50|", " 60|", " 70|", " 80|",
    " 90|", "100|"
  ]
  ledgers = [item.ledger for item in categories]
  total_withdrawn = 0
  for lg in ledgers:
    total_withdrawn += sum(
      [item["amount"] for item in lg if item["amount"] < 0])

  for cat in categories:
    part = sum([item["amount"] for item in cat.ledger if item["amount"] < 0])
    percent = math.floor((part * 100 / total_withdrawn))

    fill_range = int(percent / 10) + 1
    for i in percent_bar:
      index = percent_bar.index(i)
      if index < fill_range:
        percent_bar[index] = percent_bar[index] + " o "
      else:
        percent_bar[index] = percent_bar[index] + "   "

  full_print = "Percentage spent by category\n"
  for i in reversed(percent_bar):
    full_print += i + "\n"

  full_print += "    " + "-" * (3 * len(categories) + 1) + "\n"

  names = ' '.join(cat.name for cat in categories)
  for x in zip_longest(*names.split(), fillvalue=' '):
    full_print += "     " + '  '.join(x) + "\n"

  return full_print.rstrip("\n")
