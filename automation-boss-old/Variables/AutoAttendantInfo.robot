*** Settings ***
Library  String
Library	   OperatingSystem

*** Variables ***
&{AA_00}    Aa_Name=Test_AA     Aa_Location=random      Aa_Extension=blank    neg_test=True
&{AA_01}    Aa_Name=Test_AA     Aa_Location=random
&{AA_02}    Aa_Name=Test_AA1    AA_customExtension={rand_int}      Aa_Location=random
&{AA_03}    Aa_Name=Test_AA2    Aa_privateExtension=yes    Aa_Location=random
&{AA_04}    Aa_Name=Test_AA3    AA_customExtension={rand_int}      Aa_privateExtension=yes    Aa_Location=random
&{AA_05}    Aa_Name=Test_AA4    Aa_Location=random      Aa_assignDID=random
&{AA_06}    Aa_Name=Test_AA5     Aa_Location=random
&{AA_07}    Aa_Name=Test_AA6    AA_customExtension={rand_int}      Aa_Location=random
&{AA_08}    Aa_Name=Test_AA7    Aa_privateExtension=yes    Aa_Location=random
&{AA_09}    Aa_Name=Test_AA8    AA_customExtension={rand_int}      Aa_privateExtension=yes    Aa_Location=random
&{AA_10}    Aa_Name=Test_AA9    Aa_Location=random      Aa_assignDID=random
&{AA_11}    Aa_Name=Test_AA10     Aa_Location=random    timeout=blank