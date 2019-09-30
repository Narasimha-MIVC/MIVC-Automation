*** Settings ***
Library  String
Library	   OperatingSystem

Resource   LoginDetails.robot

*** Variables ***
&{PG_01}    Pg_Name=Test_Pg     Pg_Location=random
&{PG_02}    Pg_Name=Test_Pg1    Pg_Location=random    Pg_privateExtension=yes
&{PG_03}    Pg_Name=Test_Pg2    Pg_Location=random    Pg_Extension={rand_int}
&{PG_04}    Pg_Name=Test_Pg3    Pg_Location=random    Pg_Extension={rand_int}    Pg_privateExtension=yes
&{PG_05}    Pg_Name=Test_Pg4     Pg_Location=random
&{PG_06}    Pg_Name=Test_Pg5    Pg_Location=random    Pg_privateExtension=yes
&{PG_07}    Pg_Name=Test_Pg6    Pg_Location=random    Pg_Extension={rand_int}
&{PG_08}    Pg_Name=Test_Pg7    Pg_Location=random    Pg_Extension={rand_int}    Pg_privateExtension=yes
