import wave_client_api as waveClient
from PyQt5 import QtWidgets
import re
import requests
from bs4 import BeautifulSoup

class Client():
	def __init__(self):
		self.businessIds = {}
		self.customersIds = {}
		self.itemsIds = {}
	
	def get_businesses(self, ui):
		self.businessIds = {}
		ui.businessCBox.clear()

		token = ui.fullAccessEntry.text()
		if token != '':
			response = waveClient.get_businesses(token)
			if response['errors']:
				pass
			else:
				for idx, item in enumerate(response['data']):
					self.businessIds[idx] = {'id':item['id']}
					ui.businessCBox.addItem(item['name'])

	def get_customers(self, ui):
		self.customersIds = {}
		ui.customerCBox.clear()

		token = ui.fullAccessEntry.text()
		if ui.businessCBox.currentIndex() in self.businessIds:
			businessId = self.businessIds[ui.businessCBox.currentIndex()]['id']
		else:
			businessId = None

		if token != '' and businessId:
			response = waveClient.list_customers(token, businessId)
			if response['errors']:
				pass
			else:

				for idx, item in enumerate(response['data']):
					self.customersIds[idx] = item
					ui.customerCBox.addItem(item['email'])
					#ui.customerNameLabel.setText(item['name'])

	def customer_changed(self, ui):
		idx = ui.customerCBox.currentIndex()
		if idx in self.customersIds:
			customerName = self.customersIds[idx]['name']
			ui.customerNameLabel.setText(customerName)

	def get_items(self, ui):
		self.itemsIds = {}
		ui.itemsCBox.clear()
		ui.itemsTable.setRowCount(0)

		token = ui.fullAccessEntry.text()
		if ui.businessCBox.currentIndex() in self.businessIds:
			businessId = self.businessIds[ui.businessCBox.currentIndex()]['id']
		else:
			businessId = None

		if token != '' and businessId:
			response = waveClient.list_products(token, businessId)
			if response['errors']:
				pass
			else:
				for idx, item in enumerate(response['data']):
					self.itemsIds[idx] = {
						'id':item['id'],
						'name': item['name'],
						'description': item['description'],
						'unitPrice': item['unitPrice']
						}
					ui.itemsCBox.addItem(item['name'])

	def add_item(self, ui):
		item = self.itemsIds[ui.itemsCBox.currentIndex()]
		row_position = ui.itemsTable.rowCount()
		ui.itemsTable.insertRow(row_position)

        # Agregar widgets QLineEdit para que el usuario pueda ingresar la información del producto
		idItem = QtWidgets.QLineEdit()
		idItem.setText(item['id'])

		name_edit = QtWidgets.QLabel(item['name'])
        #name_edit.setPlaceholderText("Name")

		description_edit = QtWidgets.QLineEdit()
		description_edit.setText(item['description'])
        #description_edit.setPlaceholderText("Description")

		qty_edit = QtWidgets.QLineEdit()
		qty_edit.setText('1')
        #qty_edit.setPlaceholderText("Quantity")

		value_edit = QtWidgets.QLineEdit()
		value_edit.setText(item['unitPrice'])
        #value_edit.setPlaceholderText("Value")

		ui.itemsTable.setCellWidget(row_position, 0, idItem)
		ui.itemsTable.setCellWidget(row_position, 1, name_edit)
		ui.itemsTable.setCellWidget(row_position, 2, description_edit)
		ui.itemsTable.setCellWidget(row_position, 3, qty_edit)
		ui.itemsTable.setCellWidget(row_position, 4, value_edit) 

	def load_recipients(self, ui, path_file=''):
		try:
			if path_file == '':
			    file_path, _ = QtWidgets.QFileDialog.getOpenFileName(ui, "Select File", "", "Text Files (*.txt)")
			else:
			    file_path = path_file
			# Leer el contenido del archivo de texto
			with open(file_path, 'r') as file:
			    content = file.readlines()

			ui.recipientsLBox.clear()
			# Agregar las direcciones de correo electrónico al QListWidget
			for line in content:
			    # Utilizar una expresión regular para buscar direcciones de correo electrónico en la línea
			    matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line)

			    # Si se encontró una dirección de correo electrónico, agregarla al QListWidget
			    if len(matches) > 0:
			        ui.recipientsLBox.addItem(matches[0])
		except Exception as e:
			raise e

	def start_send_invoices(self, ui, sendThread):
		if not check_licence():
			print('\nNOT_AUTHORIZED\n')
			return
		if ui.fullAccessEntry.text() == '' or ui.recipientsLBox.count() < 1 or ui.itemsTable.rowCount() < 1:
			return
		ui.left_frame.setEnabled(False)
		ui.right_frame.setEnabled(False)
		self.sendThread = sendThread
		self.sendThread.start()
		self.sendThread.finished.connect(lambda: self.on_send_thread_finished(ui))

	def on_send_thread_finished(self, ui):
		ui.left_frame.setEnabled(True)
		ui.right_frame.setEnabled(True)

	def process_invoice(self, ui):
		accessToken = ui.fullAccessEntry.text()
		businessId = self.businessIds[ui.businessCBox.currentIndex()]['id']
		customerId = self.customersIds[ui.customerCBox.currentIndex()]['id']

		response = self.create_invoice(ui, accessToken, businessId, customerId)

		if response['data']:
			invoiceId = response['data'][0]['id']
			response2 = self.approve_invoice(accessToken, invoiceId)
			if response2['data']:
				response3 = self.send_invoice(ui, accessToken, invoiceId)
				print(response3)
	
	def create_invoice(self, ui, accessToken, businessId, customerId):
		items = self.format_items_table(ui)
		return waveClient.create_invoice(accessToken, businessId, customerId, items)

	def approve_invoice(self, accessToken, invoiceId):
		return waveClient.approve_invoice(accessToken, invoiceId)

	def send_invoice(self, ui, accessToken, invoiceId):
		to = self.get_recipients_list(ui)
		message = ui.note_entry.text()
		attachPDF = ui.attachPDFCheck.isChecked()
		emailSubject = ui.emailSubjectEntry.text()

		return waveClient.send_invoice(accessToken, invoiceId, to, emailSubject, message, attachPDF)

	def get_recipients_list(self, ui):
		items = []
		for index in range(ui.recipientsLBox.count()):
		    item = ui.recipientsLBox.item(index)
		    items.append(item.text())
		return items

	def format_items_table(self, ui):
		items = []
		for row in range(ui.itemsTable.rowCount()):
			items.append({
				'productId':ui.itemsTable.cellWidget(row, 0).text(),
				'quantity':ui.itemsTable.cellWidget(row, 3).text(),
				'unitPrice':ui.itemsTable.cellWidget(row, 4).text(),
				'description':ui.itemsTable.cellWidget(row, 2).text()
			})
		return items

	def new_customer(self, ui, form):
		if ui.businessCBox.currentIndex() in self.businessIds:
			self.newCustomerFrm = form
			self.newCustomerFrm.show()

	def send_new_customer(self, ui):

		if self.newCustomerFrm.text_name.text() != '' and ui.businessCBox.currentIndex() in self.businessIds:
			accessToken = ui.fullAccessEntry.text()
			businessId = self.businessIds[ui.businessCBox.currentIndex()]['id']

			#
			countryCode = self.newCustomerFrm.combo_countryCode.currentData()
			provinceCode = (countryCode+'-'+
					self.newCustomerFrm.combo_provinceCode.currentData())
			customerDict = {
				"name": self.newCustomerFrm.text_name.text(),
			    "firstName": self.newCustomerFrm.text_firstName.text(),
			    "lastName": self.newCustomerFrm.text_lastName.text(),
			    "email": self.newCustomerFrm.text_email.text(),
			    "phone": self.newCustomerFrm.text_phone.text(),
			    "address": {
			      "city": self.newCustomerFrm.text_city.text(),
			      "postalCode": self.newCustomerFrm.text_postalCode.text(),
			      "provinceCode": provinceCode,
			      "countryCode": countryCode
			    },
			    "currency": self.newCustomerFrm.combo_currency.currentData()
			}

			response = waveClient.create_customer(accessToken, businessId, customerDict)
			if response['errors']:
				print('Errors: ', response['errors'])
			else:
				print('Customer added')
				
			self.get_customers(ui)
			self.newCustomerFrm.close()

	def get_accounts(self, ui, onlyData=None):
		accessToken = ui.fullAccessEntry.text()
		businessId = self.businessIds[ui.businessCBox.currentIndex()]['id']

		response = waveClient.get_accounts(accessToken, businessId)
		if onlyData:
			if response['errors']:
				print('Errors: ', response['errors'])
			else:
				return response['data'][::-1]

	def new_item(self, ui, form):
		if ui.businessCBox.currentIndex() in self.businessIds:
			self.newItemFrm = form
			self.newItemFrm.show()

	def send_new_item(self, ui):
		itemName = self.newItemFrm.text_name.text() 
		itemDescription = self.newItemFrm.text_description.text()
		itemPrice = self.newItemFrm.text_unitPrice.text()
		accountId = self.newItemFrm.combo_account.currentData()

		if itemName != '' and itemPrice != '' and ui.businessCBox.currentIndex() in self.businessIds:
			accessToken = ui.fullAccessEntry.text()
			businessId = self.businessIds[ui.businessCBox.currentIndex()]['id']

			try:
				float(itemPrice)
			except:
				itemPrice = 0.0

			itemDict = {
				"name": itemName,
				"description": itemDescription,
				"unitPrice": itemPrice
			}

			response = waveClient.create_product(accessToken, businessId, accountId, itemDict)
			if response['errors']:
				print('Errors: ', response['errors'])
			else:
				print('Item added')
				
			self.get_items(ui)
			self.newItemFrm.close()

# verifica que el usuario este autorizado
def check_licence(user='huzu'):
	url = f'https://raw.githubusercontent.com/akkalame/paypal-auto-api/develop/licencias/{user}.txt'
	response = requests.get(url)
	try:
		soup = BeautifulSoup(response.content, 'html.parser')
		expire_time = int(soup.get_text())
		return expire_time > time_now() 
	except Exception as e:
		with open('error.log', 'a') as f:
			f.write(str(e)+'\n')
		return False

def time_now():
	url = f'https://unixtime.org/'
	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')
	return int(soup.find('div', class_='epoch h1').get_text())