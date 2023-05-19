import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import re
from main import Client
import os
import json

currency_codes = "USD, AUD, BRL, CAD, CNY, CZK, DKK, EUR, HKD, HUF, ILS, JPY, MYR, MXN, TWD, NZD, NOK, PHP, PLN, GBP, RUB, SGD, SEK, CHF, THB"
currencies = [
    ('United States Dollar (USD)', 'USD'),
    ('Canadian Dollar (CAD)', 'CAD'),
    ('Euro (EUR)', 'EUR'),
    ('British Pound (GBP)', 'GBP'),
    ('Australian Dollar (AUD)', 'AUD'),
    ('Japanese Yen (JPY)', 'JPY'),
    ('Swiss Franc (CHF)', 'CHF'),
    ('New Zealand Dollar (NZD)', 'NZD'),
    ('Mexican Peso (MXN)', 'MXN'),
    ('Singapore Dollar (SGD)', 'SGD'),
    ('Brazilian Real (BRL)', 'BRL'),
    ('Indian Rupee (INR)', 'INR'),
    ('Russian Ruble (RUB)', 'RUB'),
    ('South African Rand (ZAR)', 'ZAR'),
    ('Chinese Yuan (CNY)', 'CNY'),
    ('Hong Kong Dollar (HKD)', 'HKD'),
    ('Indonesian Rupiah (IDR)', 'IDR'),
    ('Israeli New Shekel (ILS)', 'ILS'),
    ('Malaysian Ringgit (MYR)', 'MYR'),
    ('Philippine Peso (PHP)', 'PHP'),
    ('Thai Baht (THB)', 'THB'),
    ('Turkish Lira (TRY)', 'TRY'),
    ('Argentine Peso (ARS)', 'ARS'),
    ('Chilean Peso (CLP)', 'CLP'),
    ('Colombian Peso (COP)', 'COP'),
    ('Danish Krone (DKK)', 'DKK'),
    ('Egyptian Pound (EGP)', 'EGP'),
    ('Icelandic Krona (ISK)', 'ISK'),
    ('Nigerian Naira (NGN)', 'NGN'),
    ('Polish Zloty (PLN)', 'PLN'),
    ('Saudi Riyal (SAR)', 'SAR'),
    ('South Korean Won (KRW)', 'KRW'),
    ('Swedish Krona (SEK)', 'SEK'),
    ('Taiwan Dollar (TWD)', 'TWD'),
    ('Ukrainian Hryvnia (UAH)', 'UAH'),
    ('United Arab Emirates Dirham (AED)', 'AED'),
    ('Uruguayan Peso (UYU)', 'UYU'),
    ('Vietnamese Dong (VND)', 'VND'),
    ('Norwegian Krone (NOK)', 'NOK'),
    ('Czech Koruna (CZK)', 'CZK'),
    ('Hungarian Forint (HUF)', 'HUF'),
    ('Romanian Leu (RON)', 'RON'),
    ('Croatian Kuna (HRK)', 'HRK'),
    ('Bulgarian Lev (BGN)', 'BGN'),
    ('New Taiwan Dollar (TWD)', 'TWD'),
    ('Qatari Rial (QAR)', 'QAR'),
    ('Peruvian Sol (PEN)', 'PEN'),
    ('New Israeli Sheqel (ILS)', 'ILS'),
    ('Moroccan Dirham (MAD)', 'MAD'),
    ('Kuwaiti Dinar (KWD)', 'KWD'),
    ('Omani Rial (OMR)', 'OMR'),
    ('Costa Rican Colón (CRC)', 'CRC'),
    ('Dominican Peso (DOP)', 'DOP'),
    ('Jordanian Dinar (JOD)', 'JOD'),
    ('Kazakhstani Tenge (KZT)', 'KZT'),
    ('Panamanian Balboa (PAB)', 'PAB'),
    ('Paraguayan Guarani (PYG)', 'PYG'),
    ('Uruguayan Peso en Unidades Indexadas (UYI)', 'UYI'),
    ('Moldovan Leu (MDL)', 'MDL'),
    ('Georgian Lari (GEL)', 'GEL'),
    ('Bahraini Dinar (BHD)', 'BHD'),
    ('Honduran Lempira (HNL)', 'HNL'),
    ('Macedonian Denar (MKD)', 'MKD'),
    ('Mauritian Rupee (MUR)', 'MUR'),
    ('Albanian Lek (ALL)', 'ALL'),
    ('Bangladeshi Taka (BDT)', 'BDT'),
    ('Belarusian Ruble (BYN)', 'BYN'),
    ('Botswana Pula (BWP)', 'BWP'),
    ('Brunei Dollar (BND)', 'BND'),
    ('Burundian Franc (BIF)', 'BIF'),
    ('Cambodian Riel (KHR)', 'KHR'),
    ('Cape Verdean Escudo (CVE)', 'CVE'),
    ('Cayman Islands Dollar (KYD)', 'KYD'),
    ('Central African CFA Franc (XAF)', 'XAF'),
    ('CFA Franc (XOF)', 'XOF'),
    ('Comorian Franc (KMF)', 'KMF'),
    ('Congolese Franc (CDF)', 'CDF'),
    ('Convertible Mark (BAM)', 'BAM'),
    ('Cuban Convertible Peso (CUC)', 'CUC'),
    ('Cuban Peso (CUP)', 'CUP'),
    ('Djiboutian Franc (DJF)', 'DJF'),
    ('East Caribbean Dollar (XCD)', 'XCD'),
    ('Eritrean Nakfa (ERN)', 'ERN'),
    ('Ethiopian Birr (ETB)', 'ETB'),
    ('Falkland Islands Pound (FKP)', 'FKP'),
    ('Fijian Dollar (FJD)', 'FJD'),
    ('Gambian Dalasi (GMD)', 'GMD'),
    ('Ghanaian Cedi (GHS)', 'GHS'),
    ('Guatemalan Quetzal (GTQ)', 'GTQ'),
    ('Guinean Franc (GNF)', 'GNF'),
    ('Guyanese Dollar (GYD)', 'GYD'),
    ('Haitian Gourde (HTG)', 'HTG'),
    ('Iraqi Dinar (IQD)', 'IQD'),
    ('Iranian Rial (IRR)', 'IRR'),
    ('Jamaican Dollar (JMD)', 'JMD'),
    ('Kenyan Shilling (KES)', 'KES'),
    ('Kyrgyzstani Som (KGS)', 'KGS'),
    ('Lao Kip (LAK)', 'LAK'),
    ('Lebanese Pound (LBP)', 'LBP'),
    ('Lesotho Loti (LSL)', 'LSL'),
    ('Liberian Dollar (LRD)', 'LRD'),
    ('Libyan Dinar (LYD)', 'LYD'),
    ('Malagasy Ariary (MGA)', 'MGA'),
    ('Malawian Kwacha (MWK)', 'MWK'),
    ('Maldivian Rufiyaa (MVR)', 'MVR'),
    ('Mauritanian Ouguiya (MRU)', 'MRU'),
    ('Mongolian Tögrög (MNT)', 'MNT'),
    ('Myanmar Kyat (MMK)', 'MMK'),
    ('Namibian Dollar (NAD)', 'NAD'),
    ('Nepalese Rupee (NPR)', 'NPR'),
    ('Nicaraguan Córdoba (NIO)', 'NIO'),
    ('North Korean Won (KPW)', 'KPW'),
    ('Pakistani Rupee (PKR)', 'PKR'),
    ('Papua New Guinean Kina (PGK)', 'PGK'),
    ('Rwandan Franc (RWF)', 'RWF'),
    ('Saint Helena Pound (SHP)', 'SHP'),
    ('Samoan Tala (WST)', 'WST'),
    ('São Tomé and Príncipe Dobra (STN)', 'STN'),
    ('Serbian Dinar (RSD)', 'RSD'),
    ('Seychellois Rupee (SCR)', 'SCR'),
    ('Sierra Leonean Leone (SLL)', 'SLL'),
    ('Solomon Islands Dollar (SBD)', 'SBD'),
    ('Somali Shilling (SOS)', 'SOS'),
    ('South Sudanese Pound (SSP)', 'SSP'),
    ('Sudanese Pound (SDG)', 'SDG'),
    ('Surinamese Dollar (SRD)', 'SRD'),
    ('Syrian Pound (SYP)', 'SYP'),
    ('Tajikistani Somoni (TJS)', 'TJS'),
    ('Tanzanian Shilling (TZS)', 'TZS'),
    ('Tongan Paʻanga (TOP)', 'TOP'),
    ('Trinidad and Tobago Dollar (TTD)', 'TTD'),
    ('Tunisian Dinar (TND)', 'TND'),
    ('Ugandan Shilling (UGX)', 'UGX'),
    ('Uzbekistani Som (UZS)', 'UZS'),
    ('Vanuatu Vatu (VUV)', 'VUV'),
    ('Venezuelan Bolívar (VES)', 'VES'),
    ('West African CFA Franc (XOF)', 'XOF'),
    ('Yemeni Rial (YER)', 'YER'),
    ('Zambian Kwacha (ZMW)', 'ZMW'),
    ('Zimbabwean Dollar (ZWL)', 'ZWL')
]
"""
('Afghanistan', 'AF'),
    ('Åland Islands', 'AX'),
    ('Albania', 'AL'),
    ('Algeria', 'DZ'),
    ('American Samoa', 'AS'),
    ('Andorra', 'AD'),
    ('Angola', 'AO'),
    ('Anguilla', 'AI'),
    ('Antarctica', 'AQ'),
    ('Antigua and Barbuda', 'AG'),
    ('Argentina', 'AR'),
    ('Armenia', 'AM'),
    ('Aruba', 'AW'),
    ('Australia', 'AU'),
    ('Austria', 'AT'),
    ('Azerbaijan', 'AZ'),
    ('Bahamas', 'BS'),
    ('Bahrain', 'BH'),
    ('Bangladesh', 'BD'),
    ('Barbados', 'BB'),
    ('Belarus', 'BY'),
    ('Belgium', 'BE'),
    ('Belize', 'BZ'),
    ('Benin', 'BJ'),
    ('Bermuda', 'BM'),
    ('Bhutan', 'BT'),
    ('Bolivia', 'BO'),
    ('Bosnia and Herzegovina', 'BA'),
    ('Botswana', 'BW'),
    ('Bouvet Island', 'BV'),
    ('Brazil', 'BR'),
    ('British Indian Ocean Territory', 'IO'),
    ('Brunei Darussalam', 'BN'),
    ('Bulgaria', 'BG'),
    ('Burkina Faso', 'BF'),
    ('Burundi', 'BI'),
    ('Cambodia', 'KH'),
    ('Cameroon', 'CM'),
    ('Cape Verde', 'CV'),
    ('Cayman Islands', 'KY'),
    ('Central African Republic', 'CF'),
    ('Chad', 'TD'),
    ('Chile', 'CL'),
    ('China', 'CN'),
    ('Christmas Island', 'CX'),
    ('Cocos (Keeling) Islands', 'CC'),
    ('Colombia', 'CO'),
    ('Comoros', 'KM'),
    ('Congo', 'CG'),
    ('Congo, The Democratic Republic of the', 'CD'),
    ('Cook Islands', 'CK'),
    ('Costa Rica', 'CR'),
    ('Côte d\'Ivoire', 'CI'),
    ('Croatia', 'HR'),
    ('Cuba', 'CU'),
    ('Cyprus', 'CY'),
    ('Czech Republic', 'CZ'),
    ('Denmark', 'DK'),
    ('Djibouti', 'DJ'),
    ('Dominica', 'DM'),
    ('Dominican Republic', 'DO'),
    ('Ecuador', 'EC'),
    ('Egypt', 'EG'),
    ('El Salvador', 'SV'),
    ('Equatorial Guinea', 'GQ'),
    ('Eritrea', 'ER'),
    ('Estonia', 'EE'),
    ('Ethiopia', 'ET'),
    ('Falkland Islands (Malvinas)', 'FK'),
    ('Faroe Islands', 'FO'),
    ('Fiji', 'FJ'),
    ('Finland', 'FI'),
    ('France', 'FR'),
    ('French Guiana', 'GF'),
    ('French Polynesia', 'PF'),
    ('French Southern Territories', 'TF'),
    ('Gabon', 'GA'),
    ('Gambia', 'GM'),
    ('Georgia', 'GE'),
    ('Germany', 'DE'),
    ('Ghana', 'GH'),
    ('Gibraltar', 'GI'),
    ('Greece', 'GR'),
    ('Greenland', 'GL'),
    ('Grenada', 'GD'),
    ('Guadeloupe', 'GP'),
    ('Guam', 'GU'),
    ('Guatemala', 'GT'),
    ('Guernsey', 'GG'),
    ('Guinea', 'GN'),
    ('Guinea-Bissau', 'GW'),
    ('Guyana', 'GY'),
    ('Haiti', 'HT'),
    ('Heard Island and McDonald Islands', 'HM'),
    ('Holy See (Vatican City State)', 'VA'),
    ('Honduras', 'HN'),
    ('Hong Kong', 'HK'),
    ('Hungary', 'HU'),
    ('Iceland', 'IS'),
    ('India', 'IN'),
    ('Indonesia', 'ID'),
    ('Iran, Islamic Republic of', 'IR'),
    ('Iraq', 'IQ'),
    ('Ireland', 'IE'),
    ('Isle of Man', 'IM'),
    ('Israel', 'IL'),
    ('Italy', 'IT'),
    ('Jamaica', 'JM'),
    ('Japan', 'JP'),
    ('Jersey', 'JE'),
    ('Jordan', 'JO'),
    ('Kazakhstan', 'KZ'),
    ('Kenya', 'KE'),
    ('Kiribati', 'KI'),
    ('Korea, Democratic People\'s Republic of', 'KP'),
    ('Korea, Republic of', 'KR'),
    ('Kuwait', 'KW'),
    ('Kyrgyzstan', 'KG'),
    ('Lao People\'s Democratic Republic', 'LA'),
    ('Latvia', 'LV'),
    ('Lebanon', 'LB'),
    ('Lesotho', 'LS'),
    ('Liberia', 'LR'),
    ('Libyan Arab Jamahiriya', 'LY'),
    ('Liechtenstein', 'LI'),
    ('Lithuania', 'LT'),
    ('Luxembourg', 'LU'),
    ('Macao', 'MO'),
    ('Macedonia, The Former Yugoslav Republic of', 'MK'),
    ('Madagascar', 'MG'),
    ('Malawi', 'MW'),
    ('Malaysia', 'MY'),
    ('Maldives', 'MV'),
    ('Mali', 'ML'),
    ('Malta', 'MT'),
    ('Marshall Islands', 'MH'),
    ('Martinique', 'MQ'),
    ('Mauritania', 'MR'),
    ('Mauritius', 'MU'),
    ('Mayotte', 'YT'),
    ('Mexico', 'MX'),
    ('Micronesia, Federated States of', 'FM'),
    ('Moldova, Republic of', 'MD'),
    ('Monaco', 'MC'),
    ('Mongolia', 'MN'),
    ('Montenegro', 'ME'),
    ('Montserrat', 'MS'),
    ('Morocco', 'MA'),
    ('Mozambique', 'MZ'),
    ('Myanmar', 'MM'),
    ('Namibia', 'NA'),
    ('Nauru', 'NR'),
    ('Nepal', 'NP'),
    ('Netherlands', 'NL'),
    ('Netherlands Antilles', 'AN'),
    ('New Caledonia', 'NC'),
    ('New Zealand', 'NZ'),
    ('Nicaragua', 'NI'),
    ('Niger', 'NE'),
    ('Nigeria', 'NG'),
    ('Niue', 'NU'),
    ('Norfolk Island', 'NF'),
    ('Northern Mariana Islands', 'MP'),
    ('Norway', 'NO'),
    ('Oman', 'OM'),
    ('Pakistan', 'PK'),
    ('Palau', 'PW'),
    ('Palestinian Territory, Occupied', 'PS'),
    ('Panama', 'PA'),
    ('Papua New Guinea', 'PG'),
    ('Paraguay', 'PY'),
    ('Peru', 'PE'),
    ('Philippines', 'PH'),
    ('Pitcairn', 'PN'),
    ('Poland', 'PL'),
    ('Portugal', 'PT'),
    ('Puerto Rico', 'PR'),
    ('Qatar', 'QA'),
    ('Réunion', 'RE'),
    ('Romania', 'RO'),
    ('Russian Federation', 'RU'),
    ('Rwanda', 'RW'),
    ('Saint Barthélemy', 'BL'),
    ('Saint Helena', 'SH'),
    ('Saint Kitts and Nevis', 'KN'),
    ('Saint Lucia', 'LC'),
    ('Saint Martin', 'MF'),
    ('Saint Pierre and Miquelon', 'PM'),
    ('Saint Vincent and the Grenadines', 'VC'),
    ('Samoa', 'WS'),
    ('San Marino', 'SM'),
    ('Sao Tome and Principe', 'ST'),
    ('Saudi Arabia', 'SA'),
    ('Senegal', 'SN'),
    ('Serbia', 'RS'),
    ('Seychelles', 'SC'),
    ('Sierra Leone', 'SL'),
    ('Singapore', 'SG'),
    ('Slovakia', 'SK'),
    ('Slovenia', 'SI'),
    ('Solomon Islands', 'SB'),
    ('Somalia', 'SO'),
    ('South Africa', 'ZA'),
    ('South Georgia and the South Sandwich Islands', 'GS'),
    ('Spain', 'ES'),
    ('Sri Lanka', 'LK'),
    ('Sudan', 'SD'),
    ('Suriname', 'SR'),
    ('Svalbard and Jan Mayen', 'SJ'),
    ('Swaziland', 'SZ'),
    ('Sweden', 'SE'),
    ('Switzerland', 'CH'),
    ('Syrian Arab Republic', 'SY'),
    ('Taiwan, Province of China', 'TW'),
    ('Tajikistan', 'TJ'),
    ('Tanzania, United Republic of', 'TZ'),
    ('Thailand', 'TH'),
    ('Timor-Leste', 'TL'),
    ('Togo', 'TG'),
    ('Tokelau', 'TK'),
    ('Tonga', 'TO'),
    ('Trinidad and Tobago', 'TT'),
    ('Tunisia', 'TN'),
    ('Turkey', 'TR'),
    ('Turkmenistan', 'TM'),
    ('Turks and Caicos Islands', 'TC'),
    ('Tuvalu', 'TV'),
    ('Uganda', 'UG'),
    ('Ukraine', 'UA'),
    ('United Arab Emirates', 'AE'),
    ('United Kingdom', 'GB'),
    ('United States Minor Outlying Islands', 'UM'),
    ('Uruguay', 'UY'),
    ('Uzbekistan', 'UZ'),
    ('Vanuatu', 'VU'),
    ('Venezuela', 'VE'),
    ('Viet Nam', 'VN'),
    ('Virgin Islands, British', 'VG'),
    ('Virgin Islands, U.S.', 'VI'),
    ('Wallis and Futuna', 'WF'),
    ('Western Sahara', 'EH'),
    ('Yemen', 'YE'),
    ('Zambia', 'ZM'),
    ('Zimbabwe', 'ZW')
"""
countries = [
    ('Canada', 'CA'),
    ('United States', 'US')   
]
provinces = {
    'US': [
        ('Alabama', 'AL'),
        ('Alaska', 'AK'),
        ('Arizona', 'AZ'),
        ('Arkansas', 'AR'),
        ('California', 'CA'),
        ('Colorado', 'CO'),
        ('Connecticut', 'CT'),
        ('Delaware', 'DE'),
        ('Florida', 'FL'),
        ('Georgia', 'GA'),
        ('Hawaii', 'HI'),
        ('Idaho', 'ID'),
        ('Illinois', 'IL'),
        ('Indiana', 'IN'),
        ('Iowa', 'IA'),
        ('Kansas', 'KS'),
        ('Kentucky', 'KY'),
        ('Louisiana', 'LA'),
        ('Maine', 'ME'),
        ('Maryland', 'MD'),
        ('Massachusetts', 'MA'),
        ('Michigan', 'MI'),
        ('Minnesota', 'MN'),
        ('Mississippi', 'MS'),
        ('Missouri', 'MO'),
        ('Montana', 'MT'),
        ('Nebraska', 'NE'),
        ('Nevada', 'NV'),
        ('New Hampshire', 'NH'),
        ('New Jersey', 'NJ'),
        ('New Mexico', 'NM'),
        ('New York', 'NY'),
        ('North Carolina', 'NC'),
        ('North Dakota', 'ND'),
        ('Ohio', 'OH'),
        ('Oklahoma', 'OK'),
        ('Oregon', 'OR'),
        ('Pennsylvania', 'PA'),
        ('Rhode Island', 'RI'),
        ('South Carolina', 'SC'),
        ('South Dakota', 'SD'),
        ('Tennessee', 'TN'),
        ('Texas', 'TX'),
        ('Utah', 'UT'),
        ('Vermont', 'VT'),
        ('Virginia', 'VA'),
        ('Washington', 'WA'),
        ('West Virginia', 'WV'),
        ('Wisconsin', 'WI'),
        ('Wyoming', 'WY')
    ],
    'CA': [
        ('Alberta', 'AB'),
        ('British Columbia', 'BC'),
        ('Manitoba', 'MB'),
        ('New Brunswick', 'NB'),
        ('Newfoundland and Labrador', 'NL'),
        ('Northwest Territories', 'NT'),
        ('Nova Scotia', 'NS'),
        ('Nunavut', 'NU'),
        ('Ontario', 'ON'),
        ('Prince Edward Island', 'PE'),
        ('Quebec', 'QC'),
        ('Saskatchewan', 'SK'),
        ('Yukon', 'YT')
    ]
}


colores = {"azul":"#2196F3", "rojo":"#FF5722", "verde":"#4CAF50"}
testing = False

__title__ = 'Wave Client API'
__version__ = '1.2.0'

class SendThread(QThread):
    finished = pyqtSignal()

    def __init__(self, parent, client):
        super().__init__()
        self.mainApp = parent
        self.client = client

    def run(self):
        self.send()
        self.finished.emit()

    def send(self):
        self.client.process_invoice(self.mainApp)

class SendReminderThread(QThread):
    finished = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.mainApp = parent

    def run(self):
        self.send()
        self.finished.emit()

    def send(self):
        print('creando invoice object')
        self.mainApp.label_information.setText("Starting")
        invoices = Invoices()

        print('obteniendo bearer token')
        self.mainApp.label_information.setText("Getting token")
        response = invoices.get_bearer_token(self.mainApp.client_id_entry.text(), self.mainApp.secret_entry.text())
        if response:
            print(response)
            return
        print('getting invoices')
        page = 1
        self.mainApp.label_information.setText(f"Getting list of invoices, Page {page}")
        list_invoices = invoices.list_invoices(page=page)
        with open('test.json', 'w') as f:
            f.write(json.dumps(list_invoices))
        
        status_can_reminder = ['UNPAID', 'SENT', 'PARTIALLY_PAID']
        while list_invoices != {}:
            total_invoices = len(list_invoices['items'])

            if total_invoices > self.mainApp.listbox_cc.count() and self.mainApp.listbox_cc.count() > 0:
                restante = total_invoices - self.mainApp.listbox_cc.count()
                for i in range(restante):
                    self.mainApp.listbox_cc.addItem(self.mainApp.listbox_cc.item(i).text())

            for idx, item in enumerate(list_invoices['items']):
                if not item['status'] in status_can_reminder:
                    print('not in status')
                    continue
                cc = (self.mainApp.listbox_cc.item(idx).text().strip().split(',')
                        if self.mainApp.listbox_cc.count() > 0 else [])
                self.mainApp.label_information.setText(f"Sending reminder {idx+1}/{total_invoices}. Page {page}")
                
                response = invoices.send_reminder(id_invoice=item['id'], 
                        subject=self.mainApp.subject_reminder.text(), 
                        note=self.mainApp.note_reminder.toPlainText(),
                        cc=cc)

            page += 1
            self.mainApp.label_information.setText(f"Getting list of invoices, Page {page}")
            list_invoices = invoices.list_invoices(page=page)
        
        self.mainApp.label_information.setText('The script "Send reminder" is finished')
        print('The script "Send reminder" is finished')

class DropableFilesQListWidget(QtWidgets.QListWidget):
    droped = pyqtSignal(list)

    def __init__(self):
        super().__init__();
        self.setAcceptDrops(True);
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            event.acceptProposedAction() 
        else:
             event.ignore()

    def dropEvent(self, event):

        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links=[]
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.droped.emit(links)
            
        else:
            event.ignore()

class CheckUser(QtWidgets.QDialog):
    #enviar_status = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Checking user")
        
        # Agregar widgets al diálogo
        self.username_entry = QtWidgets.QLineEdit()
        self.username_entry.setPlaceholderText("Username")
        btn_check = QtWidgets.QPushButton("Check")
        btn_check.clicked.connect(self.send_value)
        
        # Configurar el diseño del diálogo
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.username_entry)
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addItem(spacer)
        hbox.addWidget(btn_check)
        layout.addLayout(hbox)
        self.setLayout(layout)
        
        # Hacer que el diálogo sea modal y lo muestre
        self.setModal(True)
        self.exec_()

    def send_value(self):
        status = check_licence(self.username_entry.text())
        #self.enviar_status.emit(self.username_entry.text())
        #self.close()
        #print(status)
        if status:
            self.accept()
        else:
            self.reject()

class newCustomerForm(QtWidgets.QWidget):
    def __init__(self, parent, client):
        super().__init__()
        self.parent = parent
        self.client = client

        # cargar los estilos
        with open('src/estilos.css', mode='r') as f:
            estilos = f.read()
        self.setStyleSheet(estilos)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('New Customer')
        self.setGeometry(200, 200, 400, 300)

        
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Crear el widget de pestañas
        self.tabs = QtWidgets.QTabWidget(self)
        

        # boton para crear el customer
        confirmBtn = QtWidgets.QPushButton("Confirm")
        confirmBtn.clicked.connect(self.confirm)

        layout.addWidget(self.tabs)
        layout.addWidget(confirmBtn)

        # Crear las pestañas
        self.tab_informacion_basica = QtWidgets.QWidget()
        self.tab_direccion_facturacion = QtWidgets.QWidget()

        # Agregar las pestañas al widget de pestañas
        self.tabs.addTab(self.tab_informacion_basica, 'Información básica')
        self.tabs.addTab(self.tab_direccion_facturacion, 'Dirección de facturación')

        # Configurar el contenido de la pestaña "Información básica"
        self.initTabInformacionBasica()

        # Configurar el contenido de la pestaña "Dirección de facturación"
        self.initTabDireccionFacturacion()


    def initTabInformacionBasica(self):
        layout = QtWidgets.QVBoxLayout()

        # Campos de texto
        self.label_name = QtWidgets.QLabel('Name:')
        self.text_name = QtWidgets.QLineEdit()

        self.label_firstName = QtWidgets.QLabel('First Name:')
        self.text_firstName = QtWidgets.QLineEdit()

        self.label_lastName = QtWidgets.QLabel('Last Name:')
        self.text_lastName = QtWidgets.QLineEdit()

        self.label_email = QtWidgets.QLabel('Email:')
        self.text_email = QtWidgets.QLineEdit()

        self.label_phone = QtWidgets.QLabel('Phone:')
        self.text_phone = QtWidgets.QLineEdit()

        layout.addWidget(self.label_name)
        layout.addWidget(self.text_name)
        layout.addWidget(self.label_firstName)
        layout.addWidget(self.text_firstName)
        layout.addWidget(self.label_lastName)
        layout.addWidget(self.text_lastName)
        layout.addWidget(self.label_email)
        layout.addWidget(self.text_email)
        layout.addWidget(self.label_phone)
        layout.addWidget(self.text_phone)

        self.tab_informacion_basica.setLayout(layout)

    def initTabDireccionFacturacion(self):
        layout = QtWidgets.QVBoxLayout()

        # Campos de texto
        self.label_city = QtWidgets.QLabel('City:')
        self.text_city = QtWidgets.QLineEdit()

        self.label_provinceCode = QtWidgets.QLabel('Province / State:')
        self.combo_provinceCode = QtWidgets.QComboBox()

        self.label_postalCode = QtWidgets.QLabel('ZIP Code:')
        self.text_postalCode = QtWidgets.QLineEdit()

        # Combo box para seleccionar país
        self.label_countryCode = QtWidgets.QLabel('Country:')
        self.combo_countryCode = QtWidgets.QComboBox()
        self.combo_countryCode.currentIndexChanged.connect(self.load_state_code)
        for name, code in countries:
            self.combo_countryCode.addItem(name, code)

        # Combo box para seleccionar moneda
        self.label_currency = QtWidgets.QLabel('Currency:')
        self.combo_currency = QtWidgets.QComboBox()
        for name, code in currencies:
            self.combo_currency.addItem(name, code)

        layout.addWidget(self.label_countryCode)
        layout.addWidget(self.combo_countryCode)
        layout.addWidget(self.label_provinceCode)
        layout.addWidget(self.combo_provinceCode)
        layout.addWidget(self.label_city)
        layout.addWidget(self.text_city)
        layout.addWidget(self.label_postalCode)
        layout.addWidget(self.text_postalCode)
        layout.addWidget(self.label_currency)
        layout.addWidget(self.combo_currency)

        self.tab_direccion_facturacion.setLayout(layout)

    def confirm(self):
        self.client.send_new_customer(self.parent)
        
    def load_state_code(self):
        self.combo_provinceCode.clear()
        provincesList = provinces[self.combo_countryCode.currentData()]
        for name, code in provincesList:
            self.combo_provinceCode.addItem(name, code)

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(__title__+' v'+__version__)

        self.client = Client()

        self.left_frame = QtWidgets.QFrame()
        self.right_frame = QtWidgets.QFrame()
        self.create_left_widgets()
        self.create_right_widgets()

        self.label_information = QtWidgets.QLabel("")
        self.label_information.setStyleSheet('color:#060606')
        self.label_information.setAlignment(Qt.AlignCenter)

        dev_lbl = QtWidgets.QLabel("Developer: Akkalameo.o@gmail.com")
        dev_lbl.setStyleSheet('color:#060606; border: 0px;background-color: #f0f0f0')

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.left_frame)
        layout.addWidget(self.right_frame)

        main_layout = QtWidgets.QVBoxLayout()

        main_layout.addWidget(dev_lbl)
        main_layout.addLayout(layout)
        main_layout.addWidget(self.label_information)

        self.setLayout(main_layout)

        with open('src/estilos.css', mode='r') as f:
            estilos = f.read()
        self.setStyleSheet(estilos)

        self.show()

    def create_left_widgets(self):
        #####  Invoicer group
        """
        self.invoicer_group = QtWidgets.QGroupBox("Invoicer")

        business_name_label = QtWidgets.QLabel("Business Name")
        self.business_name_entry = QtWidgets.QLineEdit()
        self.business_name_entry.setPlaceholderText("Optional")

        self.email_label = QtWidgets.QLabel("Email invoicer")
        self.email_entry = QtWidgets.QLineEdit()
        self.email_entry.setPlaceholderText("Optional")
        if testing:
            self.email_entry.setText('')

        self.website_label = QtWidgets.QLabel("Website")
        self.website_entry = QtWidgets.QLineEdit()
        self.website_entry.setPlaceholderText("Optional")
        if testing:
            self.website_entry.setText('')

        self.tax_id_label = QtWidgets.QLabel("Tax ID")
        self.tax_id_entry = QtWidgets.QLineEdit()
        self.tax_id_entry.setPlaceholderText("Optional")
        if testing:
            self.tax_id_entry.setText('')

        self.phone_label = QtWidgets.QLabel("Phone (001)")
        self.phone_entry = QtWidgets.QLineEdit()
        self.phone_entry.setPlaceholderText("Optional")
        if testing:
            self.phone_entry.setText('')
        """
        ##

        #####  Client group
        self.accessGroup = QtWidgets.QGroupBox("Access Information")
        """
        self.client_id_label = QtWidgets.QLabel("Client ID")
        self.client_id_entry = QtWidgets.QLineEdit()
        if testing:
            self.client_id_entry.setText('')

        self.secret_label = QtWidgets.QLabel("Secret")
        self.secret_entry = QtWidgets.QLineEdit()
        if testing:
            self.secret_entry.setText('')
        """
        self.fullAccessLabel = QtWidgets.QLabel("Full Access Token")
        self.fullAccessEntry = QtWidgets.QLineEdit()
        if testing:
            self.fullAccessEntry.setText('')

        self.loadInformationBtn = QtWidgets.QPushButton('Load Information')
        self.loadInformationBtn.clicked.connect(self.load_information)

        # business
        self.businessLabel = QtWidgets.QLabel("Business")
        self.businessCBox = QtWidgets.QComboBox(self)
        self.businessCBox.currentIndexChanged.connect(self.load_business_information)

        # customers
        self.customerLabel = QtWidgets.QLabel("Customer")
        self.customerCBox = QtWidgets.QComboBox(self)
        self.customerCBox.currentIndexChanged.connect(lambda: self.client.customer_changed(self))
        self.customerNameLabel = QtWidgets.QLabel("")

        # botón para crear nuevos clientes
        self.newCustomerBtn = QtWidgets.QPushButton("New Customer")
        self.newCustomerBtn.clicked.connect(self.new_customer)

        #####  Body invoice

        self.note_label = QtWidgets.QLabel("Note")
        self.note_entry = QtWidgets.QLineEdit()
        self.note_entry.setPlaceholderText("Optional")
        if testing:
            self.note_entry.setText('nota de venta')

        self.emailSubjectLabel = QtWidgets.QLabel("Email Subject")
        self.emailSubjectEntry = QtWidgets.QLineEdit()

        #self.terms_label = QtWidgets.QLabel("Terms")
        #self.terms_text = QtWidgets.QTextEdit()
        #self.terms_text.setPlaceholderText("Optional")

        # Crear el QComboBox
        """
        self.label_currency = QtWidgets.QLabel("Currency")
        self.currency_cbox = QtWidgets.QComboBox(self)
        self.currency_cbox.setGeometry(50, 50, 200, 30)
        # Agregar opciones al QComboBox
        for currency_code in currency_codes.split(','):
            self.currency_cbox.addItem(currency_code)
        """

        # lista de productos
        self.itemsLabel = QtWidgets.QLabel("Items")
        self.itemsCBox = QtWidgets.QComboBox(self)

        # Crear botón para agregar nuevo producto
        self.addItemBtn = QtWidgets.QPushButton("Add Item")
        self.addItemBtn.clicked.connect(self.add_product)

        # Crear la tabla
        self.itemsTable = QtWidgets.QTableWidget()
        self.itemsTable.setColumnCount(5)
        self.itemsTable.setMinimumHeight(200)
        self.itemsTable.setMinimumWidth(430)
        self.itemsTable.setHorizontalHeaderLabels(['','Name', 'Description', 'Quantity', 'Value'])
        self.itemsTable.setColumnHidden(0, True)

        self.send_button = QtWidgets.QPushButton("Send")
        self.send_button.clicked.connect(lambda: self.client.start_send_invoices(self, 
            SendThread(self, self.client)))

        self.attachPDFCheck = QtWidgets.QCheckBox("Attach the invoice as PDF")

        # Access layout
        accessLayout = QtWidgets.QGridLayout()
        #accessLayout.addWidget(self.client_id_label, 0,0)
        #accessLayout.addWidget(self.client_id_entry, 0,1)
        #accessLayout.addWidget(self.secret_label, 1,0)
        #accessLayout.addWidget(self.secret_entry, 1,1)
        accessLayout.addWidget(self.fullAccessLabel, 0,0)
        accessLayout.addWidget(self.fullAccessEntry, 0,1)
        accessLayout.addWidget(self.loadInformationBtn, 1,0)
        self.accessGroup.setLayout(accessLayout)

        # layout invoicer
        """
        invoicer_layout = QtWidgets.QGridLayout()
        invoicer_layout.addWidget(business_name_label, 0, 0)
        invoicer_layout.addWidget(self.business_name_entry, 0, 1)
        invoicer_layout.addWidget(self.email_label, 1, 0)
        invoicer_layout.addWidget(self.email_entry, 1, 1)
        invoicer_layout.addWidget(self.website_label, 2, 0)
        invoicer_layout.addWidget(self.website_entry, 2, 1)
        invoicer_layout.addWidget(self.tax_id_label, 3, 0)
        invoicer_layout.addWidget(self.tax_id_entry, 3, 1)
        invoicer_layout.addWidget(self.phone_label, 4, 0)
        invoicer_layout.addWidget(self.phone_entry, 4, 1)
        self.invoicer_group.setLayout(invoicer_layout)
        """
        left_layout = QtWidgets.QGridLayout()
        #left_layout.addWidget(self.invoicer_group, 0, 0, 1, 2)
        left_layout.addWidget(self.accessGroup, 1, 0, 1, 2)
        left_layout.addWidget(self.businessLabel, 2,0)
        left_layout.addWidget(self.businessCBox, 2,1)
        left_layout.addWidget(self.customerLabel, 3,0)
        left_layout.addWidget(self.customerCBox, 3,1)
        left_layout.addWidget(self.newCustomerBtn, 3,2)
        left_layout.addWidget(self.customerNameLabel, 4,0)
        left_layout.addWidget(self.emailSubjectLabel, 5, 0)
        left_layout.addWidget(self.emailSubjectEntry, 5, 1)
        left_layout.addWidget(self.note_label, 6, 0)
        left_layout.addWidget(self.note_entry, 6, 1)
        
        #left_layout.addWidget(self.terms_label, 3, 0)
        #left_layout.addWidget(self.terms_text, 3, 1)
        #left_layout.addWidget(self.label_currency, 4, 0)
        #left_layout.addWidget(self.currency_cbox, 4, 1)
        left_layout.addWidget(self.itemsLabel, 7, 0)
        left_layout.addWidget(self.itemsCBox, 7, 1)
        left_layout.addWidget(self.addItemBtn, 7,2)
        left_layout.addWidget(self.itemsTable, 8, 0, 1, 2)
        left_layout.addWidget(self.attachPDFCheck, 9,0)
        left_layout.addWidget(self.send_button, 9, 1)
        
        
        

        self.left_frame.setLayout(left_layout)

    def create_right_widgets(self):
        # Creamos un QTabWidget y dos pestañas
        tabs = QtWidgets.QTabWidget()
        tab1 = QtWidgets.QWidget()
        tab2 = QtWidgets.QWidget()

        ####   tab 1

        # recipients
        self.recipientsLBox = DropableFilesQListWidget()
        self.loadRecipientsBtn = QtWidgets.QPushButton("Load recipients")
        self.loadRecipientsBtn.clicked.connect(lambda:self.client.load_recipients(self))
        self.recipientsLBox.droped.connect(lambda r: self.client.load_recipients(self, r[0]))

        """
        # cc
        self.listbox_cc = DropableFilesQListWidget()
        self.load_cc_button = QtWidgets.QPushButton("Load cc")
        self.load_cc_button.clicked.connect(lambda:self.load_cc(''))
        self.listbox_cc.droped.connect(lambda r: self.load_cc(r[0]))

        # names recipients
        self.listbox_names = DropableFilesQListWidget()
        self.load_names_button = QtWidgets.QPushButton("Load Names")
        self.load_names_button.clicked.connect(lambda:self.load_names(''))
        self.listbox_names.droped.connect(lambda r: self.load_names(r[0]))

        # address recipients
        self.listbox_address = DropableFilesQListWidget()
        self.load_address_button = QtWidgets.QPushButton("Load address")
        self.load_address_button.clicked.connect(lambda:self.load_address(''))
        self.listbox_address.droped.connect(lambda r: self.load_address(r[0]))
        """
        right_layout = QtWidgets.QVBoxLayout(tab1)
        right_layout.addWidget(self.recipientsLBox)
        right_layout.addWidget(self.loadRecipientsBtn)
        #right_layout.addWidget(self.listbox_cc)
        #right_layout.addWidget(self.load_cc_button)
        #right_layout.addWidget(self.listbox_names)
        #right_layout.addWidget(self.load_names_button)
        #right_layout.addWidget(self.listbox_address)
        #right_layout.addWidget(self.load_address_button)

        ####   tab 2
        #self.subject_reminder = QtWidgets.QLineEdit()
        #self.subject_reminder.setPlaceholderText("Subject")
        
        #self.cc_reminder_txtE = QtWidgets.QTextEdit()
        #self.cc_reminder_txtE.setPlaceholderText("Additional recipients (cc)")

        #self.note_reminder = QtWidgets.QTextEdit()
        #self.note_reminder.setPlaceholderText("Note to recipients")

        #btn_send_reminder = QtWidgets.QPushButton("Send Reminder")
        #btn_send_reminder.clicked.connect(self.send_reminder)

        #reminder_layout = QtWidgets.QVBoxLayout(tab2)
        #reminder_layout.addWidget(self.subject_reminder)
        #reminder_layout.addWidget(self.cc_reminder_txtE)
        #reminder_layout.addWidget(self.note_reminder)
        #reminder_layout.addWidget(btn_send_reminder)

        tabs.addTab(tab1, "Recipients Data")
        #tabs.addTab(tab2, "Reminder")
        main_right_layout = QtWidgets.QVBoxLayout()
        main_right_layout.addWidget(tabs)
        self.right_frame.setLayout(main_right_layout)

    def load_information(self):
        self.client.get_businesses(self)        

    def load_business_information(self):
        self.client.get_customers(self)
        self.client.get_items(self)

    def add_product(self):
        self.client.add_item(self)
    
    def new_customer(self):
        newCustomerFrm = newCustomerForm(self, self.client)
        self.client.new_customer(self, newCustomerFrm) 

    # en caso de que la cantidad de recipientes sea mayor al nro de names, address o cc
    # entonces se igualan en numero
    def igualar_names_address(self):
        if self.listbox.count() > self.listbox_names.count() and self.listbox_names.count() > 0:
            restante = self.listbox.count() - self.listbox_names.count()
            for i in range(restante):
                self.listbox_names.addItem(self.listbox_names.item(i).text())

        if self.listbox.count() > self.listbox_address.count() and self.listbox_address.count() > 0:
            restante = self.listbox.count() - self.listbox_address.count()
            for i in range(restante):
                self.listbox_address.addItem(self.listbox_address.item(i).text())

        if self.listbox.count() > self.listbox_cc.count() and self.listbox_cc.count() > 0:
            restante = self.listbox.count() - self.listbox_cc.count()
            for i in range(restante):
                self.listbox_cc.addItem(self.listbox_cc.item(i).text())

    def load_cc(self, path_file=''):
        try:
            if path_file == '':
                file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", "", "Text Files (*.txt)")
            else:
                file_path = path_file
            # Leer el contenido del archivo de texto
            with open(file_path, 'r') as file:
                content = file.readlines()

            self.listbox_cc.clear()
            # Agregar las direcciones de correo electrónico al QListWidget
            for line in content:
                # Utilizar una expresión regular para buscar direcciones de correo electrónico en la línea
                #matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line)

                # Si se encontró una dirección de correo electrónico, agregarla al QListWidget
                #if len(matches) > 0:
                self.listbox_cc.addItem(line)
        except Exception as e:
            pass
        #self.igualar_names_address()

    def load_names(self, path_file=''):
        try:
            if path_file == '':
                file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", "", "Text Files (*.txt)")
            else:
                file_path = path_file
            # Leer el contenido del archivo de texto
            with open(file_path, 'r') as file:
                content = file.readlines()
            
            self.listbox_names.clear()
            # Agregar las direcciones de correo electrónico al QListWidget
            for line in content:
                self.listbox_names.addItem(line)
        except:
            pass
    
    def load_address(self, path_file=''):
        try:
            if path_file == '':
                file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", "", "Text Files (*.txt)")
            else:
                file_path = path_file

            # Leer el contenido del archivo de texto
            with open(file_path, 'r') as file:
                content = file.readlines()
            self.listbox_address.clear()
            # Agregar las direcciones de correo electrónico al QListWidget
            for line in content:
                self.listbox_address.addItem(line)
        except:
            pass
    
    def send_reminder(self):
        if not check_licence():
            return
        if self.client_id_entry.text() == '' or self.secret_entry.text() == '':
            return

        self.left_frame.setEnabled(False)
        self.right_frame.setEnabled(False)
        self.send_thread = SendReminderThread(self)
        self.send_thread.start()
        self.send_thread.finished.connect(self.on_send_thread_finished)

if __name__ == '__main__':
    try:
        print('iniciando QApplication')
        app = QtWidgets.QApplication(sys.argv)
        print('instanciando app')
        window = App()
        #print('mostrando app')
        #window.show()
        
    except Exception as e:
        with open('error.log', 'a') as f:
            f.write(str(e)+'\n')

    sys.exit(app.exec_())