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
		if ui.itemsCBox.currentIndex() not in self.itemsIds:
			return
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
				if not file_path:
					return
			else:
			    file_path = path_file
			# Leer el contenido del archivo de texto
			with open(file_path, 'r') as file:
			    content = file.readlines()

			ui.recipientsTBox.clear()
			recipients = ''
			# Agregar las direcciones de correo electrónico al QListWidget
			for line in content:
				# Utilizar una expresión regular para buscar direcciones de correo electrónico en la línea
				matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line)

				# Si se encontró una dirección de correo electrónico, agregarla al QListWidget
				if len(matches) > 0:
					recipients += matches[0].strip()+'\n'
			ui.recipientsTBox.setText(recipients.strip())
			
		except Exception as e:
			raise e

	def start_send_invoices(self, ui, sendThread):
		if not check_licence():
			print('\nNOT_AUTHORIZED\n')
			return
		if ui.fullAccessEntry.text() == '' or ui.recipientsTBox.toPlainText() == '' or ui.itemsTable.rowCount() < 1:
			return
		ui.left_frame.setEnabled(False)
		ui.right_frame.setEnabled(False)
		self.sendThread = sendThread
		self.sendThread.start()
		self.sendThread.finished.connect(lambda: self.on_send_thread_finished(ui))

	def on_send_thread_finished(self, ui):
		ui.left_frame.setEnabled(True)
		ui.right_frame.setEnabled(True)

	def create_invoice(self, ui, accessToken, businessId, customerId, footer):
		items = self.format_items_table(ui)
		return waveClient.create_invoice(accessToken, businessId, customerId, items, footer)

	def approve_invoice(self, accessToken, invoiceId):
		return waveClient.approve_invoice(accessToken, invoiceId)

	def send_invoice(self, ui, accessToken, invoiceId, to):
		message = ui.note_entry.toPlainText()
		attachPDF = ui.attachPDFCheck.isChecked()
		emailSubject = ui.emailSubjectEntry.text()

		return waveClient.send_invoice(accessToken, invoiceId, to, emailSubject, message, attachPDF)

	def process_invoice(self, ui):
		accessToken = ui.fullAccessEntry.text()
		businessId = self.businessIds[ui.businessCBox.currentIndex()]['id']
		customerId = self.customersIds[ui.customerCBox.currentIndex()]['id']
		footer = ui.footerEntry.text()

		response = self.create_invoice(ui, accessToken, businessId, customerId, footer)

		if response['data']:
			recipientsList = self.get_recipients_list(ui)
			for idx, to in enumerate(recipientsList):
				if response['data']:
					if response['data'][0]:
						invoiceId = response['data'][0]['id']
						response2 = self.approve_invoice(accessToken, invoiceId)
						if response2['data']:
							response3 = self.send_invoice(ui, accessToken, invoiceId, to)
							if response3['data']:
								if 'didSucceed' in response3['data']:
									if response3['data']['didSucceed']:
										print(f'Sent part {idx+1}/{len(recipientsList)}')
									else:
										print('Fail to send reminder')
								else:
									print(response2['data'])
							if response3['errors']:
								print('Errors: ', response3['errors'])
					else:
						print('Invalid inputs, try to set less words')
				if response['errors']:
					print('Errors: ', response['errors'])
	
	def start_send_reminders(self, ui, sendThread):
		if not check_licence():
			print('\nNOT_AUTHORIZED\n')
			return
		if ui.fullAccessEntry.text() == '' or ui.recipientsTBox.toPlainText() == '':
			return
		ui.left_frame.setEnabled(False)
		ui.right_frame.setEnabled(False)
		self.sendThread = sendThread
		self.sendThread.start()
		self.sendThread.finished.connect(lambda: self.on_send_thread_finished(ui))

	def process_reminders(self, ui):
		accessToken = ui.fullAccessEntry.text()
		if ui.businessCBox.currentIndex() in self.businessIds:
			businessId = self.businessIds[ui.businessCBox.currentIndex()]['id']
		else:
			businessId = None

		response = waveClient.list_invoices(accessToken, businessId)
		if response['data']:
			invoicesId = [r['id'] for r in response['data'] 
							if r['status'] != 'DRAFT' and r['status'] != 'CANCEL']
			recipientsList = self.get_recipients_list(ui)
			idxInvoice = 0
			for idx, to in enumerate(recipientsList):
				invoiceId = invoicesId[idxInvoice]
				response2 = self.send_reminder(ui, accessToken, invoiceId, to)
				
				if response2['data']:
					if 'didSucceed' in response2['data']:
						if response2['data']['didSucceed']:
							print(f'Reminder Sent part {idx+1}/{len(recipientsList)}')
						else:
							print('Fail to send reminder')
					else:
						print(response2['data'])
				if response2['errors']:
					print('Errors: ', response2['errors'])

				idxInvoice = idxInvoice +1 if idxInvoice < len(invoicesId)-1 else 0
	
	def send_reminder(self, ui, accessToken, invoiceId, to):
		message = ui.note_entry.toPlainText()
		emailSubject = ui.emailSubjectEntry.text()

		return waveClient.send_invoice(accessToken, invoiceId, to, emailSubject, message)

	def get_invoices(self, ui):

		token = ui.fullAccessEntry.text()
		if ui.businessCBox.currentIndex() in self.businessIds:
			businessId = self.businessIds[ui.businessCBox.currentIndex()]['id']
		else:
			businessId = None

		if token != '' and businessId:
			response = waveClient.list_invoices(token, businessId)
			if response['errors']:
				print('Errors: ', response['errors'])
			else:
				return response(response['data'])
						
	def get_recipients_list(self, ui):
		rawRecipients = ui.recipientsTBox.toPlainText().split('\n')
		recipients = [r.strip() for r in rawRecipients if is_email(r.strip()) ]
		intervalos = int(ui.nRecipientsTxt.text()) if ui.nRecipientsTxt.text() != '' else 0
		if intervalos > 0:
			return dividir_array(recipients, intervalos)

		return recipients

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

	def new_multi_cus_item(self, ui, form, createThread):
		self.newMultiCusItemFrm = form
		self.newMultiCusItemFrm.create.connect(lambda: self.start_create_multi_cus_item(ui, createThread))
		self.newMultiCusItemFrm.show()

	def start_create_multi_cus_item(self, ui, thread):
		self.createMultiCusItemThread = thread
		self.createMultiCusItemThread.start()

	def process_multi_item_cus(self, ui):
		if not self.validate_multi_cus_item():
			print('You need to fill all Name\'s fields')
			return

		tokens = [r.strip() for r in 
				self.newMultiCusItemFrm.tokensTBox.toPlainText().strip().split('\n')]

		if len(tokens) > 0:
			for token in tokens:
				print('\nGetting business of token',token)
				response = waveClient.get_businesses(token)
				if response['errors']:
					print('Error getting business\nError:',response['errors'])
				else:
					# selecting the business
					businessId = ''
					for idx, business in enumerate(response['data']):
						# set a first business as default
						if (self.newMultiCusItemFrm.personalBusinessCBox.isChecked() 
							and business['isPersonal']):
							businessId = business['id']
							break
						else:
							businessId = business['id']
							break

					# creating new customer
					print('Creating new customer')

					countryCode = self.newMultiCusItemFrm.combo_countryCode.currentData()
					provinceCode = (countryCode+'-'+
							self.newMultiCusItemFrm.combo_provinceCode.currentData())
					customerDict = {
						"name": self.newMultiCusItemFrm.customerName.text(),
					    "firstName": self.newMultiCusItemFrm.text_firstName.text(),
					    "lastName": self.newMultiCusItemFrm.text_lastName.text(),
					    "email": self.newMultiCusItemFrm.text_email.text(),
					    "phone": self.newMultiCusItemFrm.text_phone.text(),
					    "address": {
					      "city": self.newMultiCusItemFrm.text_city.text(),
					      "postalCode": self.newMultiCusItemFrm.text_postalCode.text(),
					      "provinceCode": provinceCode,
					      "countryCode": countryCode
					    },
					    "currency": self.newMultiCusItemFrm.combo_currency.currentData()
					}

					customerResponse = waveClient.create_customer(token, businessId, customerDict)
					if customerResponse['errors']:
						print('Error Making customer to token',token)
						print('Errors: ', customerResponse['errors'])
					else:
						print('Customer added')

					# getting the account id
					accountsResponse = waveClient.get_accounts(token, businessId)
					accountId = ''
					if accountsResponse['errors']:
						print('Error Getting account')
						print('Errors: ', accountsResponse['errors'])
					else:
						for account in accountsResponse['data']:
							accountId = account['id']
							if account['subtype']['value'] == 'INCOME':
								break

					if not accountId:
						print('Not have account available to items in token',token)
						continue

					# creating new item
					itemName = self.newMultiCusItemFrm.itemName.text() 
					itemDescription = self.newMultiCusItemFrm.text_description.text()
					itemPrice = self.newMultiCusItemFrm.text_unitPrice.text()
					#accountId = self.newMultiCusItemFrm.combo_account.currentData()

					try:
						float(itemPrice)
					except:
						itemPrice = 0.0

					itemDict = {
						"name": itemName,
						"description": itemDescription,
							"unitPrice": itemPrice
						}

					itemResponse = waveClient.create_product(token, businessId, accountId, itemDict)
					if itemResponse['errors']:
						print('Errors: ', itemResponse['errors'])
					else:
						print('Item added')


	def validate_multi_cus_item(self):
		if self.newMultiCusItemFrm.customerName.text() == '':
			return False

		if self.newMultiCusItemFrm.itemName.text() == '':
			return False

		return True

def is_email(texto):
	# Expresión regular para verificar el formato de un correo electrónico
	patron = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	return re.match(patron, texto) is not None

def dividir_array(array, limite):
	array_dividido = [array[i:i+limite] for i in range(0, len(array), limite)]
	return array_dividido

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