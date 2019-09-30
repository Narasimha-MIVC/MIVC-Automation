*** Variables ***
#PhoneSystem ---> Phone Number
&{PhoneNumber_Assign}          tn_status=Pending port in        tn_type=Domestic            display_name=-
&{PhoneNumber_Assign01}         tn_status=Pending port in        tn_type=Global Inbound     display_name=-
&{PhoneNumber_Assign02}          tn_status=Pending port in        tn_type=Global Toll Free      display_name=-
&{PhoneNumber_Assign03}        tn_status=Available              tn_type=Global Inbound      display_name=-
&{PhoneNumber_Assign04}          tn_status=Available              tn_type=Global Toll Free      display_name=-
&{PhoneNumber_Edit}               tn_status=Pending port in        dest_type=Hunt Group      display_name=(       d_name_32={rand_str}     error_msg=Max limit of characters is 32
&{PhoneNumber_Edit01}           tn_status=Pending port in        dest_type=Hunt Group     display_name=(       error_msg=Display Name is required
&{PhoneNumber_Edit02}           tn_status=Pending port in        dest_type=Hunt Group     display_name=(

&{PhoneNumber_Assign_BCA}           tn_status=Pending port in        tn_type=Domestic       DNIS_Type=Hunt Group      display_name=-       d_name_32=TestHG

&{PhoneNumber_Export}       tn_status=Pending port in

