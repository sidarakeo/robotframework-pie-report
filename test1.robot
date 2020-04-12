*** Settings ***
Documentation     Simple example using SeleniumLibrary.
Library           SeleniumLibrary

*** Variables ***
${LOGIN URL}      http://localhost:7272
${BROWSER}        Chrome

*** Test Cases ***
Verify Login
   log     "Ahnang"
   sleep  5s
Verify homepage   
   logxxx     "Ahnang"