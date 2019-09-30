*** Settings ***
Documentation    Keyword supported for the Summit Cloud feature

Library    Collections

*** Keywords ***
I connect db
    [Documentation]  The keyword to connect to DB
    [Arguments]  &{db_connect_info}
    ${result}=  run keyword  dbconnect  &{db_connect_info}
    should be true  ${result}

I query db
    [Documentation]  The Keyword to execute a query on db
    [Arguments]  ${query}  ${result_as_dict}=${True}
    ${result}  ${data}=  run keyword  dbquery  ${query}  ${result_as_dict}
    should be true  ${result}
    [Return]  ${data}

I fetch data from summit cloud db
    [Arguments]  ${url}=${None}  &{url_components}
    ${result}  ${data}=  run keyword  sc_fetch_data  ${url}  &{url_components}
    should be true  ${result}
    [Return]  ${data}

I compare and varify ${test_data} with ${db_data} for table ${table_id}
    ${result}=  run keyword  sc_verify_db_data  ${test_data}  ${db_data}  ${table_id}
    should be true  ${result}

I verify log details of summitcloud db
    [Arguments]  ${db_id}  ${data}=${None}  &{login_credentials}
    ${result}=  run keyword  sc_verify_db_log  ${db_id}  ${data}  &{login_credentials}

In D2 I verify account ids
    [Arguments]  ${tenants_ids}  ${tenants_names}
    ${result}=   Run Keyword    director_verify_tenant_uuid   ${tenants_ids}  ${tenants_names}
    should be true  ${result}

I query summitcloud db
    [Arguments]  ${db_name}  ${query}=${None}  &{params}
    ${result}=  run keyword  sc_query_uc_db  ${db_name}  ${query}  &{params}
    should be true  ${result}

I start docker container
    [Arguments]  &{params}
    ${result}=  run keyword  sc_uc_container_manipulation  ${None}  start  &{params}
    should be true  ${result}

I stop docker container
    [Arguments]  ${db_id}  &{params}
    ${result}=  run keyword  sc_uc_container_manipulation  ${db_id}  stop  &{params}
    should be true  ${result}

I fetch data from back sync db
    [Arguments]  ${url}=${None}  &{url_components}
    ${result}  ${data}=  run keyword  backsync_fetch_data  ${url}  &{url_components}
    should be true  ${result}
    [Return]  ${data}
