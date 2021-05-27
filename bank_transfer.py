import enum
from typing import List


class Customer:
    last_id = 0

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        Customer.last_id += 1
        self.id = Customer.last_id

    def __repr__(self):
        return 'Customer[{},{},{}]'.format(self.id, self.firstname, self.lastname)


class Account:
    last_id = 0

    def __init__(self, customer):
        Account.last_id += 1
        self.id = Account.last_id
        self.customer = customer
        self._balance = 0

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print('New deposit updated as: ' + str(self._balance))
        else:
            raise NegativeAmountException("The amount is negative. Please input the positive amount")

    def charge(self, amount):
        if amount > self._balance:
            raise NotEnoughBalanceException(
                "You don't have enough Balance. Your Current Balance is " + str(self._balance))
        if amount <= 0:
            raise NegativeAmountException("The amount is negative. Please input the positive amount")
        else:
            self._balance -= amount
            print("Charge amount is: " + str(amount))
            print("New Balance updated as: " + str(self._balance))

    def __repr__(self):
        return 'Account[{},{},{}]'.format(self.id, self.customer.lastname, self._balance)


class SavingsAccount(Account):
    interest_rate = 0.01

    def calc_interest(self):
        self._balance += self.interest_rate * self._balance


class CheckingAccount(Account):
    pass


class BankException(Exception):
    pass


class NegativeAmountException(BankException):
    pass


class NotEnoughBalanceException(BankException):
    pass


class AccountNotFoundException(BankException):
    pass


class Bank:
    class AccountType(enum.Enum):
        SAVINGS_ACCOUNT = enum.auto()
        CHECKING_ACCOUNT = enum.auto()

    account_type_mapper = {
        AccountType.SAVINGS_ACCOUNT: SavingsAccount,
        AccountType.CHECKING_ACCOUNT: CheckingAccount
    }

    def __init__(self):
        self.customers: List[Customer] = []
        self.accounts: List[Account] = []

    # Customer Factory
    def new_customer(self, first_name, last_name):
        c = Customer(first_name, last_name)
        self.customers.append(c)
        return c

    # Add account factory to bank
    def new_account(self, account_type: AccountType, customer):
        account = self.account_type_mapper[account_type](customer)
        self.accounts.append(account)
        return account

    # Implement transfer
    def transfer(self, from_acc_id, to_acc_id, amount):
        try:
            from_account = self._get_account(from_acc_id)
            to_account = self._get_account(to_acc_id)
            from_account.charge(amount)
            to_account.deposit(amount)
            print(f'Transferred {amount} successfully from {from_acc_id} to {to_account}!')
        except BankException as e:
            print(e)

    def _get_account(self, account_id):
        for account in self.accounts:
            if account.id == account_id:
                return account
        raise AccountNotFoundException("Account with the provided id does not exist!")
#
# Commented to check if new code works
# c1 = Customer('John', 'Smith')
# print(c1)
# c2 = Customer('Anne', 'Brown')
# print(c2)
# del c2
# c2 = Customer('Anne2', 'Brown')
# print(c2)
# print(c3)
# a1 = SavingsAccount(c1)
# a2 = CheckingAccount(c2)
# print(a1)
# a1.deposit(100)
# a2.deposit(200)
# a1.calc_interest()
# print(a1)
# print(a2)
# try:
#     a1._balance = 'abc'
#     a1.calc_interest()
#     a1.charge(-200)
#     print('After charging')
#     print(a1)
# except NotEnoughBalanceException as nebe:
#     print('Exception: ' + str(nebe))
# except BankException as nebe:
#     # except BankException as nebe:
#     print('General Exception: ' + str(nebe))
# # except NegativeAmountException as nae:
# #     print('Exception: ' + str(nae))
# print('running further')

if __name__ == '__main__':
    bank = Bank()

    user1 = bank.new_customer("Dave", "Smith")
    user2 = bank.new_customer("Sonia", "Kaminsky")
    print(user1)
    print(user2)

    account_user1 = bank.new_account(Bank.AccountType.SAVINGS_ACCOUNT, user1)
    account_user2 = bank.new_account(Bank.AccountType.CHECKING_ACCOUNT, user2)

    account_user1.deposit(15000)
    account_user2.deposit(15000)
    print()
    print("ACCOUNTS BALANCES")
    print(account_user1)
    print(account_user2)
    id_user1 = 1
    id_user2 = 2
    print()
    print("TRANSFER DETAILS")
    amount_to_send = 6032
    bank.transfer(from_acc_id=id_user2, to_acc_id=id_user1, amount=amount_to_send)
    print()
    print("AFTER TRANSACTION BALANCES")
    print(account_user1)
    print(account_user2)

