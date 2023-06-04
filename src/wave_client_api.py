import requests
import json

# full access token n6VdX7P9GKjbM5lcD0W81utBgG2DDT
scope = "https://gql.waveapps.com/graphql/public"

def exceute_request(accessToken, query, variables={}):
	if query:
		headers = {
		  	'Authorization': f'Bearer {accessToken}',
		  	'Content-Type': 'application/json'
		}

		json_data = {
			'query': query,
			'variables': variables
		}
	
		return json.loads(requests.request("POST", scope, headers=headers, json=json_data).text)

def get_user(accessToken):
	query = "query { user { id defaultEmail } }"
	
	response = exceute_request(accessToken, query)
	try:
		return response['data']['user']
	except Exception as e:
		raise e

def get_businesses(accessToken):
	query = """
		query {
		  businesses(page: 1, pageSize: 10) {
		    pageInfo {
		      currentPage
		      totalPages
		      totalCount
		    }
		    edges {
		      node {
		        id
		        name
		        isClassicAccounting
		        isPersonal
		      }
		    }
		  }
		}
	"""
	response = response = exceute_request(accessToken, query)
	try:
		errors = get_errors(response)
		data = []
		if not errors:
			for edge in response['data']['businesses']['edges']:
				data.append(edge['node'])
		return {
			"data": data,
			"errors": errors
		}
			
	except Exception as e:
		raise e

def list_customers(accessToken, businessId):
	query = """
    query {{
      business(id: "{0}") {{
        id
        customers(page: 1, pageSize: 20, sort: [NAME_ASC]) {{
          pageInfo {{
            currentPage
            totalPages
            totalCount
          }}
          edges {{
            node {{
              id
              name
              email
            }}
          }}
        }}
      }}
    }}
    """.format(businessId)

	response = response = exceute_request(accessToken, query)
	try:
		errors = get_errors(response)
		data = []
		if not errors:
			for edge in response['data']['business']['customers']['edges']:
				data.append(edge['node'])

		return {
			"data": data,
			"errors": errors
		}
			
	except Exception as e:
		raise e

def list_products(accessToken, businessId):
	query = """
    query ($businessId: ID!, $page: Int!, $pageSize: Int!) {
		  business(id: $businessId) {
		    id
		    products(page: $page, pageSize: $pageSize) {
		      pageInfo {
		        currentPage
		        totalPages
		        totalCount
		      }
		      edges {
		        node {
		          id
		          name
		          description
		          unitPrice
		          defaultSalesTaxes {
		            id
		            name
		            abbreviation
		            rate
		          }
		          isSold
		          isBought
		          isArchived
		          createdAt
		          modifiedAt
		        }
		      }
		    }
		  }
		}
    """

	variables = {
	  "businessId": businessId,
	  "page": 1,
	  "pageSize": 50
	}
	response = response = exceute_request(accessToken, query, variables)
	try:
		errors = get_errors(response)
		data = []
		if not errors:
			for edge in response['data']['business']['products']['edges']:
				data.append(edge['node'])

		return {
			"data": data,
			"errors": errors
		}
			
	except Exception as e:
		raise e

def create_customer(accessToken, businessId, customer):
	query = """
		mutation ($input: CustomerCreateInput!) {
		  customerCreate(input: $input) {
		    didSucceed
		    inputErrors {
		      code
		      message
		      path
		    }
		    customer {
		      id
		      name
		      firstName
		      lastName
		      email
		      address {
		        addressLine1
		        addressLine2
		        city
		        province {
		          code
		          name
		        }
		        country {
		          code
		          name
		        }
		        postalCode
		      }
		      currency {
		        code
		      }
		    }
		  }
		}
	"""

	"""
	"name": "Santa",
		    "firstName": "Saint",
		    "lastName": "Nicholas",
		    "email": "santa@example.com",
		    "address": {
		      "city": "North Pole",
		      "postalCode": "H0H 0H0",
		      "provinceCode": "CA-NU",
		      "countryCode": "CA"
		    },
		    "currency": "CAD"
	"""
	variables = {
		"input": {
			"businessId": businessId,
		    
		}
	}

	for key in customer:
		variables['input'][key] = customer[key]
	response = response = exceute_request(accessToken, query, variables)
	try:
		errors = get_errors(response)
		data = []
		if not errors:
			data.append(response['data']['customerCreate']['customer'])
				
		return {
			"data": data,
			"errors": errors
		}
			
	except Exception as e:
		raise e

def get_accounts(accessToken, businessId):
	query = """
		query {
		  business(id: "<BUSINESS_ID>") {
		    id
		    accounts(subtypes: [INCOME, DISCOUNTS, OTHER_INCOME]) {
		      edges {
		        node {
		          id
		          name
		          subtype {
		            name
		            value
		          }
		        }
		      }
		    }
		  }
		}
	""".replace("<BUSINESS_ID>", businessId)
	response = response = exceute_request(accessToken, query)
	try:
		errors = get_errors(response)
		data = []
		if not errors:
			for edge in response['data']['business']['accounts']['edges']:
				data.append(edge['node'])
		return {
			"data": data,
			"errors": errors
		}
			
	except Exception as e:
		raise e

def create_product(accessToken, businessId, accountId, item):
	query = """
		mutation ($input: ProductCreateInput!) {
		  productCreate(input: $input) {
		    didSucceed
		    inputErrors {
		      code
		      message
		      path
		    }
		    product {
		      id
		      name
		      description
		      unitPrice
		      incomeAccount {
		        id
		        name
		      }
		      expenseAccount {
		        id
		        name
		      }
		      isSold
		      isBought
		      isArchived
		      createdAt
		      modifiedAt
		    }
		  }
		}
	"""

	
	"""item = {"name": "LED Bulb",
				    "description": "5 Watt C7 light bulb",
				    "unitPrice": "2.0625"}"""
	
	variables = {
		"input": {
			"businessId": businessId,
			"incomeAccountId": accountId,

		}
	}

	for key in item:
		variables['input'][key] = item[key]
	response = response = exceute_request(accessToken, query, variables)
	try:
		errors = get_errors(response)
		data = []
		if not errors:
			data.append(response['data']['productCreate']['product'])
				
		return {
			"data": data,
			"errors": errors
		}
			
	except Exception as e:
		raise e

def refresh_token(clientId, clientSecret, previousToken):
	scopeToken = 'https://api.waveapps.com/oauth2/token/'
	headers = {
	  	'Content-Type': 'application/x-www-form-urlencoded'
	}
	redirect_uri = 'https://api.waveapps.com/oauth2/authorize/'
	data = f'client_id={clientId}&client_secret={clientSecret}&refresh_token={previousToken}&grant_type=refresh_token&redirect_uri={redirect_uri}'
	print(data)
	return requests.request("POST", scopeToken, headers=headers, data=data).text

def create_invoice(accessToken, businessId, customerId, itemsList, footer):
	query = """
		mutation ($input: InvoiceCreateInput!) {
		  invoiceCreate(input: $input) {
		    didSucceed
		    inputErrors {
		      message
		      code
		      path
		    }
		    invoice {
		      id
		      createdAt
		      modifiedAt
		      pdfUrl
		      viewUrl
		      status
		      title
		      subhead
		      invoiceNumber
		      invoiceDate
		      poNumber
		      customer {
		        id
		        name
		      }
		      currency {
		        code
		      }
		      dueDate

		      amountDue {
		        value
		        currency {
		          symbol
		        }
		      }
		      amountPaid {
		        value
		        currency {
		          symbol
		        }
		      }
		      taxTotal {
		        value
		        currency {
		          symbol
		        }
		      }
		      total {
		        value
		        currency {
		          symbol
		        }
		      }
		      exchangeRate
		      footer
		      memo
		      disableCreditCardPayments
		      disableBankPayments
		      itemTitle
		      unitTitle
		      priceTitle
		      amountTitle
		      hideName
		      hideDescription
		      hideUnit
		      hidePrice
		      hideAmount
		      items {
		        product {
		          id
		          name
		        }
		        description
		        quantity
		        price
		        subtotal {
		          value
		          currency {
		            symbol
		          }
		        }
		        total {
		          value
		          currency {
		            symbol
		          }
		        }
		        account {
		          id
		          name
		          subtype {
		            name
		            value
		          }
		        }
		        taxes {
		          amount {
		            value
		          }
		          salesTax {
		            id
		            name
		          }
		        }
		      }
		      lastSentAt
		      lastSentVia
		      lastViewedAt
		    }
		  }
		}
	"""
	variables = {
	  "input": {
	    "businessId": businessId,
	    "customerId": customerId,
	    "items": itemsList,
	    "footer": footer,
	    
	  }
	}

	response = response = exceute_request(accessToken, query, variables)
	try:
		errors = get_errors(response)
		data = []
		if not errors:
			data.append(response['data']['invoiceCreate']['invoice'])
				
		return {
			"data": data,
			"errors": errors
		}
			
	except Exception as e:
		raise e

def approve_invoice(accessToken, invoiceId):
	query = """
		mutation ($input: InvoiceApproveInput!) {
		  invoiceApprove(input: $input) {
		    invoice {
		    	id
		    }
		    didSucceed
		    inputErrors {
		      message
		      code
		      path
		    }
		  }
		}
	"""
	variables = {
	  "input": {
	    "invoiceId": invoiceId
	  }
	}
	response = response = exceute_request(accessToken, query, variables)
	try:
		errors = get_errors(response)
		data = []
		if not errors:
			data.append(response['data']['invoiceApprove']['invoice'])
				
		return {
			"data": data,
			"errors": errors
		}
			
	except Exception as e:
		raise e

def send_invoice(accessToken, invoiceId, to, subject, message='', attachPDF=False):
	query = """
		mutation ($input: InvoiceSendInput!) {
		  invoiceSend(input: $input) {
		    didSucceed
		    inputErrors {
		      message
		      code
		      path
		    }
		  }
		}
	"""
	variables = {
	  "input": {
	    "invoiceId": invoiceId,
	    "to": to,
	    "subject": subject,
	    "message": message,
	    "attachPDF": attachPDF
	  }
	}
	response = response = exceute_request(accessToken, query, variables)
	try:
		errors = get_errors(response)
		data = []
		if not errors:
			data.append({'didSucceed': response['data']['invoiceSend']['didSucceed']})
		
		try:
			errors += response['data']['invoiceSend']['inputErrors']
		except:
			pass#print('please send picture of this to developer\nsend_invoice',response)

		return {
			"data": data,
			"errors": errors
		}
			
	except Exception as e:
		raise e

def list_invoices(accessToken, businessId):
	query = """
    query($businessId: ID!, $page: Int!, $pageSize: Int!) {
		  business(id: $businessId) {
		    id
		    invoices(page: $page, pageSize: $pageSize) {
		      pageInfo {
		        currentPage
		        totalPages
		        totalCount
		      }
		      edges {
		        node {
		          id
		          createdAt
		          modifiedAt
		          pdfUrl
		          viewUrl
		          status
		          title
		          subhead
		          invoiceNumber
		          invoiceDate
		          poNumber
		          customer {
		            id
		            name
		            # Can add additional customer fields here
		          }
		          currency {
		            code
		          }
		          dueDate
		          amountDue {
		            value
		            currency {
		              symbol
		            }
		          }
		          amountPaid {
		            value
		            currency {
		              symbol
		            }
		          }
		          taxTotal {
		            value
		            currency {
		              symbol
		            }
		          }
		          total {
		            value
		            currency {
		              symbol
		            }
		          }
		          exchangeRate
		          footer
		          memo
		          disableCreditCardPayments
		          disableBankPayments
		          itemTitle
		          unitTitle
		          priceTitle
		          amountTitle
		          hideName
		          hideDescription
		          hideUnit
		          hidePrice
		          hideAmount
		          items {
		            product {
		              id
		              name
		              # Can add additional product fields here
		            }
		            description
		            quantity
		            price
		            subtotal {
		              value
		              currency {
		                symbol
		              }
		            }
		            total {
		              value
		              currency {
		                symbol
		              }
		            }
		            account {
		              id
		              name
		              subtype {
		                name
		                value
		              }
		              # Can add additional account fields here
		            }
		            taxes {
		              amount {
		                value
		              }
		              salesTax {
		                id
		                name
		                # Can add additional sales tax fields here
		              }
		            }
		          }
		          lastSentAt
		          lastSentVia
		          lastViewedAt
		        }
		      }
		    }
		  }
		}
  """
	
	variables	= {
  	"businessId": businessId,
  	"page": 1,
  	"pageSize": 20
	} 
	response = response = exceute_request(accessToken, query, variables)
	try:
		errors = get_errors(response)
		data = []
		if not errors:
			for edge in response['data']['business']['invoices']['edges']:
				data.append(edge['node'])

		return {
			"data": data,
			"errors": errors
		}
			
	except Exception as e:
		raise e

def get_errors(response):
	if "errors" in response:
		errors = []
		for error in response['errors']:
			errors.append({
				"code": error['extensions']['code'],
				"message": error['message']
			})
		return errors
	else:
		return []

if __name__ == "__main__":
	accessToken = 'n6VdX7P9GKjbM5lcD0W81utBgG2DDT'
	businessId = 'QnVzaW5lc3M6Y2VkZGJkZTktZjhiYS00MTE2LWFmMTItNmEzYWZjMTBiMjBj'
	incomeAccount = 'QWNjb3VudDoxNzM3Njg4OTA0NTQ0MzA5MTkxO0J1c2luZXNzOmNlZGRiZGU5LWY4YmEtNDExNi1hZjEyLTZhM2FmYzEwYjIwYw=='
	customerId = 'QnVzaW5lc3M6Y2VkZGJkZTktZjhiYS00MTE2LWFmMTItNmEzYWZjMTBiMjBjO0N1c3RvbWVyOjc1MzI2NTY1'
	itemsId = [{
		'productId':'QnVzaW5lc3M6Y2VkZGJkZTktZjhiYS00MTE2LWFmMTItNmEzYWZjMTBiMjBjO1Byb2R1Y3Q6OTEwODIwODQ=',
		'quantity': 5,
		'unitPrice': 400,
		'description': 'roja'
		}]
	invoiceId = 'QnVzaW5lc3M6Y2VkZGJkZTktZjhiYS00MTE2LWFmMTItNmEzYWZjMTBiMjBjO0ludm9pY2U6MTcyODc2OTcyNjAxMzc3NTMxNA=='
	# list businesses
	#r = get_businesses('n6VdX7P9GKjbM5lcD0W81utBgG2DDT')
	#print(r)
	
	# list customers
	#r = list_customers(accessToken, businessId)
	#print(r)
	
	# create customer
	#r = create_customer(accessToken, businessId, 'customer')
	#print(r)

	# list income account
	#r = get_accounts(accessToken, businessId)
	#print(r)
	
	# list products
	#r = list_products(accessToken, businessId)

	# create product
	#r = create_product(accessToken, businessId, incomeAccount, 'item')
	#print(r)

	# create invoice
	#r = create_invoice(accessToken, businessId, customerId, itemsId)
	#print(r)

	# approve invoice
	#r = approve_invoice(accessToken, invoiceId)
	#print(r)

	# send invoice
	#r = send_invoice(accessToken, invoiceId, ['akk7@yopmail.com', 'akk6@yopmail.com'], message='mes', attachPDF=True)
	#print(r)

	# refresh token
	#clientId = '7uX4ZakwddCkq_LoSn1UFET1MCylFz0pLQ4Y.fi7'
	#clientSecret = '03fDWRTaVlrywIBpNSbBnLxKft3AAls7SEr25eYWGWUjrshGxifZZ7LcFqVxsf4EyoA6WEdcAGOC1cRF8N9ckJ1OwRNX9iI961tc2DvJKLYn61TOkx8kkf1uj4yUhtx8'
	#previousToken = 'n6VdX7P9GKjbM5lcD0W81utBgG2DDT'
	#r = refresh_token(clientId, clientSecret, previousToken)
	#print(r)