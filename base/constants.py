EMP_ROLE = 'emp'
ADMIN_ROLE = 'admin'
CUSTOMER_ROLE = 'customer'
WINERY_ROLE = 'winery'
RETAILER_ROLE = 'retailer'

ROLE_CHOICES = [
    (EMP_ROLE, 'Employee'),
    (ADMIN_ROLE, 'Admin'),
]

URL_MAPPING_FOR_VIEWSET_LIST = {
    'get': 'list',
    'post': 'create'
}

URL_MAPPING_FOR_VIEWSET_DETAIL = {
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
}