# Access Application Summary

## Overview

| Category | Count |
| --- | --- |
| Forms | 42 |
| Subforms | 5 |
| Tables | 20 |
| Querys | 360 |
| Modules | 31 |
| Controls | 1342 |
| Events | 307 |
| Procedures | 292 |
| Macros | 5 |

## Data Model

### CUSTOMER (6,049 records)

| Field | Type |
|-------|------|
| CID | Long Integer |
| Title | Text |
| Fname | Text |
| Lname | Text |
| Company | Text |
| Street1 | Text |
| City | Text |
| State | Text |
| Zip | Text |
| Source | Text |
| Map | Text |
| Grid | Text |
| Phone | Text |
| Fax | Text |
| Evening Phone | Text |
| Customer Note | Memo |
| Referance | Boolean |
| Cell Phone | Text |
| E-Mail | Memo |
| Tax Exempt | Boolean |
| Wood Chips | Boolean |
| Firewood | Boolean |

### DESCRIPTION (83 records)

| Field | Type |
|-------|------|
| DID | Long Integer |
| Descriptoin | Text |

### EVENT (8,578 records)

| Field | Type |
|-------|------|
| OID | Long Integer |
| Line No | Long Integer |
| Event_No | Double |
| Event_Date | Date/Time |
| Prod Type | Text |
| Completed | Boolean |
| Complete_Date | Date/Time |
| To Bill | Boolean |
| Billed | Boolean |
| Bill_Date | Date/Time |
| Event Price | Currency |
| Paid Date | Date/Time |
| Price | Currency |
| Paid Total | Currency |
| Total Order Price | Currency |
| Total Order Tax | Currency |
| Total Order | Currency |
| Total Accepted Price | Currency |
| Total Accepted Tax | Currency |
| Total Accepted | Currency |
| Paid in full | Boolean |
| Days Outstanding | Long Integer |
| Billed 2 | Boolean |
| Billed 3 | Boolean |
| Billed 4 | Boolean |
| Bill_Date 2 | Date/Time |
| Bill_Date 3 | Date/Time |
| Bill_Date 4 | Date/Time |
| Invoice note | Text |
| Gallonage | Long Integer |
| Invoice_Id | Long Integer |

### LOCATION (113 records)

| Field | Type |
|-------|------|
| Location | Text |

### Map data (22 records)

| Field | Type |
|-------|------|
| Street | Text |
| City | Text |

### ORDER (903 records)

| Field | Type |
|-------|------|
| OID | Long Integer |
| CID | Long Integer |
| Order | Boolean |
| Proposal Date | Date/Time |
| Accept Date | Date/Time |
| Work Street | Text |
| Work City | Text |
| Work State | Text |
| Work Zip | Text |
| Paid Amount | Currency |
| Job Note | Text |
| Office Note | Memo |
| Annual Contract | Boolean |
| Work Name | Text |
| Work Map | Long Integer |
| Work Grid | Text |
| Winter Work | Boolean |
| 2025 Accepted | Boolean |
| 2024 Accepted | Boolean |
| 2023 Accepted | Boolean |
| 2022 Accepted | Boolean |
| 2021 Accepted | Boolean |
| 2020 Accepted | Boolean |
| 2019 Accepted | Boolean |
| 2018 Accepted | Boolean |
| 2017 Accepted | Boolean |
| 2016 Accepted | Boolean |
| 2015 Accepted | Boolean |
| 2014 Accepted | Boolean |
| 2013 Accepted | Boolean |
| 2012 Accepted | Boolean |
| 2011 Accepted | Boolean |
| 2010 Accepted | Boolean |
| 2009 Accepted | Boolean |
| 2008 Accepted | Boolean |
| 2007 Accepted | Boolean |
| 2006 Accepted | Boolean |
| 2005 Accepted | Boolean |
| PrePaid Disc Given | Currency |
| Write-Off Given | Currency |
| Pd Amt 1 | Currency |
| Pd Amt 2 | Currency |
| Pd Amt 3 | Currency |
| Pd Amt 4 | Currency |
| Pd Amt 5 | Currency |
| Pd Amt 6 | Currency |
| Pd Date 1 | Date/Time |
| Pd Date 2 | Date/Time |
| Pd Date 3 | Date/Time |
| Pd Date 4 | Date/Time |
| Pd Date 5 | Date/Time |
| Pd Date 6 | Date/Time |
| Ck # 1 | Long Integer |
| Ck # 2 | Long Integer |
| Ck # 3 | Long Integer |
| Ck # 4 | Long Integer |
| Ck # 5 | Long Integer |
| Ck # 6 | Long Integer |
| Service Declined | Boolean |

### ORDER DETAIL (7,495 records)

| Field | Type |
|-------|------|
| OID | Long Integer |
| Line No | Long Integer |
| Prod Type | Text |
| Location | Text |
| Plant | Text |
| Description | Text |
| Pest | Text |
| Start | Date/Time |
| Price | Currency |
| 25 Price | Currency |
| 24 Price | Currency |
| 23 Price | Currency |
| 22 Price | Currency |
| 21 Price | Currency |
| 20 Price | Currency |
| 19 Price | Currency |
| 18 Price | Currency |
| 17 Price | Currency |
| 16 Price | Currency |
| 15 Price | Currency |
| 14 Price | Currency |
| 13 Price | Currency |
| 12 Price | Currency |
| 11 Price | Currency |
| 10 Price | Currency |
| 09 Price | Currency |
| 08 Price | Currency |
| 07 Price | Currency |
| Accept | Boolean |
| 25 Accepted | Boolean |
| 24 Accepted | Boolean |
| 23 Accepted | Boolean |
| 22 Accepted | Boolean |
| 21 Accepted | Boolean |
| 20 Accepted | Boolean |
| 19 Accepted | Boolean |
| 18 Accepted | Boolean |
| 17 Accepted | Boolean |
| 16 Accepted | Boolean |
| 15 Accepted | Boolean |
| 14 Accepted | Boolean |
| 13 Accepted | Boolean |
| 12 Accepted | Boolean |
| 11 Accepted | Boolean |
| 10 Accepted | Boolean |
| 09 Accepted | Boolean |
| 08 Accepted | Boolean |
| 07 Accepted | Boolean |
| Accepted Date | Date/Time |
| CrewID | Text |
| ScheduleDate | Date/Time |
| ScheduleReady | Boolean |
| Priority | Text |
| LargeTree | Boolean |

### OrderSource (903 records)

| Field | Type |
|-------|------|
| OID | Long Integer |
| CID | Long Integer |
| Order | Boolean |
| Proposal Date | Date/Time |
| Accept Date | Date/Time |
| Work Street | Text |
| Work City | Text |
| Work State | Text |
| Work Zip | Text |
| Paid Amount | Currency |
| Job Note | Text |
| Office Note | Memo |
| Annual Contract | Boolean |
| Work Name | Text |
| Work Map | Long Integer |
| Work Grid | Text |
| Winter Work | Boolean |
| 2025 Accepted | Boolean |
| 2024 Accepted | Boolean |
| 2023 Accepted | Boolean |
| 2022 Accepted | Boolean |
| 2021 Accepted | Boolean |
| 2020 Accepted | Boolean |
| 2019 Accepted | Boolean |
| 2018 Accepted | Boolean |
| 2017 Accepted | Boolean |
| 2016 Accepted | Boolean |
| 2015 Accepted | Boolean |
| 2014 Accepted | Boolean |
| 2013 Accepted | Boolean |
| 2012 Accepted | Boolean |
| 2011 Accepted | Boolean |
| 2010 Accepted | Boolean |
| 2009 Accepted | Boolean |
| 2008 Accepted | Boolean |
| 2007 Accepted | Boolean |
| 2006 Accepted | Boolean |
| 2005 Accepted | Boolean |
| PrePaid Disc Given | Currency |
| Write-Off Given | Currency |
| Pd Amt 1 | Currency |
| Pd Amt 2 | Currency |
| Pd Amt 3 | Currency |
| Pd Amt 4 | Currency |
| Pd Amt 5 | Currency |
| Pd Amt 6 | Currency |
| Pd Date 1 | Date/Time |
| Pd Date 2 | Date/Time |
| Pd Date 3 | Date/Time |
| Pd Date 4 | Date/Time |
| Pd Date 5 | Date/Time |
| Pd Date 6 | Date/Time |
| Ck # 1 | Long Integer |
| Ck # 2 | Long Integer |
| Ck # 3 | Long Integer |
| Ck # 4 | Long Integer |
| Ck # 5 | Long Integer |
| Ck # 6 | Long Integer |
| Service Declined | Boolean |

### PEST (215 records)

| Field | Type |
|-------|------|
| Pest | Text |

### PLANT (174 records)

| Field | Type |
|-------|------|
| Plant | Text |

### PRODUCT (11 records)

| Field | Type |
|-------|------|
| Prod Type | Text |
| Prod Desc | Text |

### Paste Errors (1 records)

| Field | Type |
|-------|------|
| Field0 | Memo |

### Payments (504 records)

| Field | Type |
|-------|------|
| PaymentID | Long Integer |
| OrderID | Long Integer |
| ScheduledSprayID | Long Integer |
| CID | Long Integer |
| PaymentDate | Date/Time |
| AmountPaid | Currency |
| PaidIndex | Byte |
| Notes | Text |

### STATE (14 records)

| Field | Type |
|-------|------|
| State | Text |
| State Name | Text |

### Scheduled Sprays (9 records)

| Field | Type |
|-------|------|
| F1 | Double |
| F2 | Double |
| F3 | Double |
| F4 | Text |
| F5 | Text |
| F6 | Double |
| F7 | Text |
| F8 | Text |
| F9 | Text |
| F10 | Text |
| F11 | Text |
| F12 | Text |
| F13 | Currency |
| F14 | Text |
| F15 | Text |
| F16 | Text |
| F17 | Text |
| F18 | Date/Time |
| F19 | Text |
| F20 | Text |
| F21 | Text |
| F22 | Text |
| F23 | Text |
| F24 | Text |
| F25 | Text |
| F26 | Text |
| F27 | Text |
| F28 | Text |
| F29 | Text |
| F30 | Text |
| F31 | Text |
| F32 | Text |
| F33 | Text |
| F34 | Text |
| F35 | Text |
| F36 | Text |
| F37 | Text |
| F38 | Text |
| F39 | Text |
| F40 | Text |
| F41 | Text |
| F42 | Text |
| F43 | Text |
| F44 | Text |
| F45 | Text |
| F46 | Text |
| F47 | Text |
| F48 | Text |
| F49 | Text |
| F50 | Text |
| F51 | Text |
| F52 | Text |
| F53 | Text |
| F54 | Text |
| F55 | Text |
| F56 | Text |
| F57 | Text |
| F58 | Text |
| F59 | Text |
| F60 | Text |
| F61 | Text |
| F62 | Text |
| F63 | Text |
| F64 | Text |
| F65 | Text |
| F66 | Text |
| F67 | Text |
| F68 | Text |
| F69 | Text |
| F70 | Text |
| F71 | Text |
| F72 | Text |
| F73 | Text |
| F74 | Text |
| F75 | Text |
| F76 | Text |
| F77 | Text |
| F78 | Text |
| F79 | Text |
| F80 | Text |
| F81 | Text |
| F82 | Text |
| F83 | Text |
| F84 | Text |
| F85 | Text |
| F86 | Text |
| F87 | Text |
| F88 | Text |
| F89 | Text |
| F90 | Text |
| F91 | Text |
| F92 | Text |
| F93 | Text |
| F94 | Text |
| F95 | Text |
| F96 | Text |
| F97 | Text |
| F98 | Text |
| F99 | Text |
| F100 | Text |
| F101 | Text |
| F102 | Text |
| F103 | Text |
| F104 | Text |
| F105 | Text |
| F106 | Text |
| F107 | Text |
| F108 | Text |
| F109 | Text |
| F110 | Text |
| F111 | Text |
| F112 | Text |
| F113 | Text |
| F114 | Text |
| F115 | Text |
| F116 | Text |
| F117 | Text |
| F118 | Text |
| F119 | Text |
| F120 | Text |
| F121 | Text |
| F122 | Text |
| F123 | Text |
| F124 | Text |
| F125 | Text |
| F126 | Text |
| F127 | Text |
| F128 | Text |
| F129 | Text |
| F130 | Text |
| F131 | Text |
| F132 | Text |
| F133 | Text |
| F134 | Text |
| F135 | Text |
| F136 | Text |
| F137 | Text |
| F138 | Text |
| F139 | Text |
| F140 | Text |
| F141 | Text |
| F142 | Text |
| F143 | Text |
| F144 | Text |
| F145 | Text |
| F146 | Text |
| F147 | Text |
| F148 | Text |
| F149 | Text |
| F150 | Text |
| F151 | Text |
| F152 | Text |
| F153 | Text |
| F154 | Text |
| F155 | Text |
| F156 | Text |
| F157 | Text |
| F158 | Text |
| F159 | Text |
| F160 | Text |
| F161 | Text |
| F162 | Text |
| F163 | Text |
| F164 | Text |
| F165 | Text |
| F166 | Text |
| F167 | Text |
| F168 | Text |
| F169 | Text |
| F170 | Text |
| F171 | Text |
| F172 | Text |
| F173 | Text |
| F174 | Text |
| F175 | Text |
| F176 | Text |
| F177 | Text |
| F178 | Text |
| F179 | Text |
| F180 | Text |
| F181 | Text |
| F182 | Text |
| F183 | Text |
| F184 | Text |
| F185 | Text |
| F186 | Text |
| F187 | Text |
| F188 | Text |
| F189 | Text |
| F190 | Text |
| F191 | Text |
| F192 | Text |
| F193 | Text |
| F194 | Text |
| F195 | Text |
| F196 | Text |
| F197 | Text |
| F198 | Text |
| F199 | Text |
| F200 | Text |
| F201 | Text |
| F202 | Text |
| F203 | Text |
| F204 | Text |
| F205 | Text |
| F206 | Text |
| F207 | Text |
| F208 | Text |
| F209 | Text |
| F210 | Text |
| F211 | Text |
| F212 | Text |
| F213 | Text |
| F214 | Text |
| F215 | Text |
| F216 | Text |
| F217 | Text |
| F218 | Text |
| F219 | Text |
| F220 | Text |
| F221 | Text |
| F222 | Text |
| F223 | Text |
| F224 | Text |
| F225 | Text |
| F226 | Text |
| F227 | Text |
| F228 | Text |
| F229 | Text |
| F230 | Text |
| F231 | Text |
| F232 | Text |
| F233 | Text |
| F234 | Text |
| F235 | Text |
| F236 | Text |
| F237 | Text |
| F238 | Text |
| F239 | Text |
| F240 | Text |
| F241 | Text |
| F242 | Text |
| F243 | Text |
| F244 | Text |
| F245 | Text |
| F246 | Text |
| F247 | Text |
| F248 | Text |
| F249 | Text |
| F250 | Text |
| F251 | Text |
| F252 | Text |
| F253 | Text |
| F254 | Text |
| F255 | Text |

### Scheduled Sprays1 (14 records)

| Field | Type |
|-------|------|
| F1 | Double |
| F2 | Double |
| F3 | Double |
| F4 | Text |
| F5 | Text |
| F6 | Double |
| F7 | Text |
| F8 | Text |
| F9 | Text |
| F10 | Text |
| F11 | Text |
| F12 | Text |
| F13 | Currency |
| F14 | Text |
| F15 | Text |
| F16 | Text |
| F17 | Text |
| F18 | Date/Time |
| F19 | Text |
| F20 | Text |
| F21 | Text |
| F22 | Text |
| F23 | Text |
| F24 | Text |
| F25 | Text |
| F26 | Text |
| F27 | Text |
| F28 | Text |
| F29 | Text |
| F30 | Text |
| F31 | Text |
| F32 | Text |
| F33 | Text |
| F34 | Text |
| F35 | Text |
| F36 | Text |
| F37 | Text |
| F38 | Text |
| F39 | Text |
| F40 | Text |
| F41 | Text |
| F42 | Text |
| F43 | Text |
| F44 | Text |
| F45 | Text |
| F46 | Text |
| F47 | Text |
| F48 | Text |
| F49 | Text |
| F50 | Text |
| F51 | Text |
| F52 | Text |
| F53 | Text |
| F54 | Text |
| F55 | Text |
| F56 | Text |
| F57 | Text |
| F58 | Text |
| F59 | Text |
| F60 | Text |
| F61 | Text |
| F62 | Text |
| F63 | Text |
| F64 | Text |
| F65 | Text |
| F66 | Text |
| F67 | Text |
| F68 | Text |
| F69 | Text |
| F70 | Text |
| F71 | Text |
| F72 | Text |
| F73 | Text |
| F74 | Text |
| F75 | Text |
| F76 | Text |
| F77 | Text |
| F78 | Text |
| F79 | Text |
| F80 | Text |
| F81 | Text |
| F82 | Text |
| F83 | Text |
| F84 | Text |
| F85 | Text |
| F86 | Text |
| F87 | Text |
| F88 | Text |
| F89 | Text |
| F90 | Text |
| F91 | Text |
| F92 | Text |
| F93 | Text |
| F94 | Text |
| F95 | Text |
| F96 | Text |
| F97 | Text |
| F98 | Text |
| F99 | Text |
| F100 | Text |
| F101 | Text |
| F102 | Text |
| F103 | Text |
| F104 | Text |
| F105 | Text |
| F106 | Text |
| F107 | Text |
| F108 | Text |
| F109 | Text |
| F110 | Text |
| F111 | Text |
| F112 | Text |
| F113 | Text |
| F114 | Text |
| F115 | Text |
| F116 | Text |
| F117 | Text |
| F118 | Text |
| F119 | Text |
| F120 | Text |
| F121 | Text |
| F122 | Text |
| F123 | Text |
| F124 | Text |
| F125 | Text |
| F126 | Text |
| F127 | Text |
| F128 | Text |
| F129 | Text |
| F130 | Text |
| F131 | Text |
| F132 | Text |
| F133 | Text |
| F134 | Text |
| F135 | Text |
| F136 | Text |
| F137 | Text |
| F138 | Text |
| F139 | Text |
| F140 | Text |
| F141 | Text |
| F142 | Text |
| F143 | Text |
| F144 | Text |
| F145 | Text |
| F146 | Text |
| F147 | Text |
| F148 | Text |
| F149 | Text |
| F150 | Text |
| F151 | Text |
| F152 | Text |
| F153 | Text |
| F154 | Text |
| F155 | Text |
| F156 | Text |
| F157 | Text |
| F158 | Text |
| F159 | Text |
| F160 | Text |
| F161 | Text |
| F162 | Text |
| F163 | Text |
| F164 | Text |
| F165 | Text |
| F166 | Text |
| F167 | Text |
| F168 | Text |
| F169 | Text |
| F170 | Text |
| F171 | Text |
| F172 | Text |
| F173 | Text |
| F174 | Text |
| F175 | Text |
| F176 | Text |
| F177 | Text |
| F178 | Text |
| F179 | Text |
| F180 | Text |
| F181 | Text |
| F182 | Text |
| F183 | Text |
| F184 | Text |
| F185 | Text |
| F186 | Text |
| F187 | Text |
| F188 | Text |
| F189 | Text |
| F190 | Text |
| F191 | Text |
| F192 | Text |
| F193 | Text |
| F194 | Text |
| F195 | Text |
| F196 | Text |
| F197 | Text |
| F198 | Text |
| F199 | Text |
| F200 | Text |
| F201 | Text |
| F202 | Text |
| F203 | Text |
| F204 | Text |
| F205 | Text |
| F206 | Text |
| F207 | Text |
| F208 | Text |
| F209 | Text |
| F210 | Text |
| F211 | Text |
| F212 | Text |
| F213 | Text |
| F214 | Text |
| F215 | Text |
| F216 | Text |
| F217 | Text |
| F218 | Text |
| F219 | Text |
| F220 | Text |
| F221 | Text |
| F222 | Text |
| F223 | Text |
| F224 | Text |
| F225 | Text |
| F226 | Text |
| F227 | Text |
| F228 | Text |
| F229 | Text |
| F230 | Text |
| F231 | Text |
| F232 | Text |
| F233 | Text |
| F234 | Text |
| F235 | Text |
| F236 | Text |
| F237 | Text |
| F238 | Text |
| F239 | Text |
| F240 | Text |
| F241 | Text |
| F242 | Text |
| F243 | Text |
| F244 | Text |
| F245 | Text |
| F246 | Text |
| F247 | Text |
| F248 | Text |
| F249 | Text |
| F250 | Text |
| F251 | Text |
| F252 | Text |
| F253 | Text |
| F254 | Text |
| F255 | Text |

### TEMP TABLE1 (20 records)

| Field | Type |
|-------|------|
| Sequence | Double |
| Oid | Long Integer |
| Line | Long Integer |
| Lname | Text |
| Street | Text |
| Map | Long Integer |
| City | Text |
| Grid | Text |
| Phone | Text |
| Location | Text |
| Plant | Text |
| Pest | Text |
| Price | Currency |
| Product | Text |
| Cust info | Text |
| Job Info | Text |
| Company Name | Text |
| Date | Date/Time |
| Prod | Text |
| Operator | Text |

### TREATMENT_DETAIL (233 records)

| Field | Type |
|-------|------|
| TID | Long Integer |
| Line No | Integer |
| Time of Year Start | Date/Time |
| For Pest | Text |

### Titles (13 records)

| Field | Type |
|-------|------|
| Title | Text |

### tblCrewAssignments (0 records)

| Field | Type |
|-------|------|
| AssignID | Long Integer |
| OID | Long Integer |
| LineNo | Long Integer |
| Crew | Text |
| Priority | Text |
| RouteOrder | Long Integer |
| ScheduleDate | Date/Time |
| Notes | Text |
| Selected | Boolean |

## Form Hierarchy

- **Custnoteform**
- **Invoice SwitchBoard**
- **OrderSwitchBoard**
- **YEAR END SWITCHBOARD**
- **Pest**
- **SpraySwitchBoard**
- **TreeSwitchBoard**
- **Customer 2**
- **Job Note**
- **frmInvoiceGenerator**
- **SwitchBoard11**
- **subfrmTotalReceivables**
- **SwitchBoard1a**
- **App_PPHM_Completed**
- **App_Spray_Completed**
- **frmSuperScheduler**
  - **frmSuperSchedulerSub** _(via frmSuperSchedulerSub)_
  - **frmCrew1Sub** _(via frmCrew1Sub)_
  - **frmCrew2Sub** _(via frmCrew2Sub)_
- **ORDER EDIT**
  - **ORDER_DETAIL** _(via ORDER_DETAIL)_
- **Plant**
- **SwitchBoard1**
- **SwitchBoard2**
- **Cust form**
- **INVOICE EDIT FORM**
  - **ORDER_DETAIL_INVOICE2** _(via ORDER_DETAIL_INVOICE2)_
- **SwitchBoard**
- **Treatment**
  - **Treatment Detail** _(via Treatment Detail)_
- **Customer**
- **Customer 3**
- **Copy of ORDER**
  - **ORDER_DETAIL** _(via ORDER_DETAIL)_
- **DESCRIPTION**
- **ORDER**
  - **ORDER_DETAIL** _(via ORDER_DETAIL)_
- **ORDER_DET_DISP**
  - **ORDER_DET_DISP_EVENT** _(via ORDER_DET_DISP_EVENT)_
- **Chemical**
- **Events To Do**
- **ORDER EDIT1**
  - **ORDER_DETAIL** _(via ORDER_DETAIL)_
- **Invoice SwitchBoard1**
- **TOTALS**
- **Invoice SwitchBoard2**
- **SwitchboardAccountsReceivable**
- **frmCustomerFilterTest2**
  - **frmCustomerSubFormTest** _(via frmCustomerSubFormTest)_
- **frmCustomerFilterTest1**

## Navigation Flows

- `frmSuperScheduler.cmbLname` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmbLname` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmbCity` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmbCity` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmbZip` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmbZip` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmbMap` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmbMap` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmbGrid` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmbGrid` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmbPriority` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmbPriority` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmdReset` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmdReset` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmdMapCrew1` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmdMapCrew1` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmdScheduleCrew1` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmdScheduleCrew1` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmdScheduleCrew2` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmdScheduleCrew2` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmdMapCrew2` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmdMapCrew2` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmbPest` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmbPest` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmbProdType` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmbProdType` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmbCrew` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmbCrew` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmdDateBack` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmdDateBack` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmdDateForward` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmdDateForward` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmdUpdateScheduling` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmdUpdateScheduling` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmbLargeTree` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmbLargeTree` → opens → `rptMissingStartDates`
- `frmSuperScheduler.cmbStartDate` → opens → `rptCrewSchedule`
- `frmSuperScheduler.cmbStartDate` → opens → `rptMissingStartDates`
- `SwitchBoard1.opens Orderswitchboardform` → opens → `SwitchboardAccountsReceivable`
- `SwitchBoard1.Openssprayswitchboard` → opens → `SwitchboardAccountsReceivable`
- `SwitchBoard1.Opens the Invoice Switchboard` → opens → `SwitchboardAccountsReceivable`
- `SwitchBoard1.Command49` → opens → `SwitchboardAccountsReceivable`
- `SwitchBoard1.Command51` → opens → `SwitchboardAccountsReceivable`
- `SwitchBoard1.Command52` → opens → `SwitchboardAccountsReceivable`
- `SwitchBoard1.AccountsReceivableButton` → opens → `SwitchboardAccountsReceivable`
- `SwitchboardAccountsReceivable.Command69` → opens → `rptReceivablesByClient`
- `SwitchboardAccountsReceivable.Command69` → opens → `rptReceivablesDetails`
- `SwitchboardAccountsReceivable.Command69` → opens → `Switchboard1`
- `SwitchboardAccountsReceivable.Command69` → opens → `rptAcctsRcbvl2`
- `SwitchboardAccountsReceivable.Command77` → opens → `rptReceivablesByClient`
- `SwitchboardAccountsReceivable.Command77` → opens → `rptReceivablesDetails`
- `SwitchboardAccountsReceivable.Command77` → opens → `Switchboard1`
- `SwitchboardAccountsReceivable.Command77` → opens → `rptAcctsRcbvl2`
- `SwitchboardAccountsReceivable.Command78` → opens → `rptReceivablesByClient`
- `SwitchboardAccountsReceivable.Command78` → opens → `rptReceivablesDetails`
- `SwitchboardAccountsReceivable.Command78` → opens → `Switchboard1`
- `SwitchboardAccountsReceivable.Command78` → opens → `rptAcctsRcbvl2`

## Key VBA Procedures (by outgoing CALLS)

| Procedure | Outgoing Calls |
|-----------|----------------|
| frmSuperScheduler_cmbLname_AfterUpdate | 21 |
| frmSuperScheduler_cmbCity_AfterUpdate | 21 |
| frmSuperScheduler_cmbZip_AfterUpdate | 21 |
| frmSuperScheduler_cmbMap_AfterUpdate | 21 |
| frmSuperScheduler_cmbGrid_AfterUpdate | 21 |
| frmSuperScheduler_cmbPriority_AfterUpdate | 21 |
| frmSuperScheduler_cmdReset_OnClick | 21 |
| frmSuperScheduler_cmdMapCrew1_OnClick | 21 |
| frmSuperScheduler_cmdScheduleCrew1_OnClick | 21 |
| frmSuperScheduler_cmdScheduleCrew2_OnClick | 21 |

## Dead Controls (no events, no control source)

- `App_PPHM_Completed` / `Text10`
- `App_PPHM_Completed` / `Text12`
- `App_PPHM_Completed` / `Text18`
- `App_PPHM_Completed` / `Text20`
- `App_PPHM_Completed` / `Text33`
- `App_PPHM_Completed` / `Text34`
- `App_PPHM_Completed` / `Text7`
- `App_PPHM_Completed` / `Text8`
- `App_Spray_Completed` / `Text10`
- `App_Spray_Completed` / `Text12`
- `App_Spray_Completed` / `Text18`
- `App_Spray_Completed` / `Text20`
- `App_Spray_Completed` / `Text33`
- `App_Spray_Completed` / `Text34`
- `App_Spray_Completed` / `Text7`
- `App_Spray_Completed` / `Text8`
- `Chemical` / `Text10`
- `Chemical` / `Text7`
- `Chemical` / `Text8`
- `Copy of ORDER` / `Box45`
- `Copy of ORDER` / `Box60`
- `Copy of ORDER` / `Evening`
- `Copy of ORDER` / `Frame128`
- `Copy of ORDER` / `Frame130`
- `Copy of ORDER` / `Frame134`
- `Copy of ORDER` / `Label129`
- `Copy of ORDER` / `Label131`
- `Copy of ORDER` / `Label132`
- `Copy of ORDER` / `Label135`
- `Copy of ORDER` / `Label139`
- `Copy of ORDER` / `Label141`
- `Copy of ORDER` / `Label152`
- `Copy of ORDER` / `Label156`
- `Copy of ORDER` / `Label157`
- `Copy of ORDER` / `Label158`
- `Copy of ORDER` / `Label160`
- `Copy of ORDER` / `Label161`
- `Copy of ORDER` / `Label177`
- `Copy of ORDER` / `Label179`
- `Copy of ORDER` / `Label183`
- `Copy of ORDER` / `Label184`
- `Copy of ORDER` / `Label185`
- `Copy of ORDER` / `Label186`
- `Copy of ORDER` / `Label187`
- `Copy of ORDER` / `Label188`
- `Copy of ORDER` / `Label189`
- `Copy of ORDER` / `Label190`
- `Copy of ORDER` / `Label191`
- `Copy of ORDER` / `Label192`
- `Copy of ORDER` / `Label194`
- `Copy of ORDER` / `Label196`
- `Copy of ORDER` / `Label198`
- `Copy of ORDER` / `Label200`
- `Copy of ORDER` / `Label202`
- `Copy of ORDER` / `Label204`
- `Copy of ORDER` / `Label206`
- `Copy of ORDER` / `Label208`
- `Copy of ORDER` / `Label210`
- `Copy of ORDER` / `Label212`
- `Copy of ORDER` / `Label214`
- `Copy of ORDER` / `Label216`
- `Copy of ORDER` / `Label218`
- `Copy of ORDER` / `Label220`
- `Copy of ORDER` / `Label222`
- `Copy of ORDER` / `Label224`
- `Copy of ORDER` / `Label226`
- `Copy of ORDER` / `Label228`
- `Copy of ORDER` / `Label230`
- `Copy of ORDER` / `Label232`
- `Copy of ORDER` / `Label234`
- `Copy of ORDER` / `Label236`
- `Copy of ORDER` / `Label243`
- `Copy of ORDER` / `ORDER_DETAIL`
- `Copy of ORDER` / `Text124`
- `Copy of ORDER` / `Text18`
- `Copy of ORDER` / `Text34`
- `Copy of ORDER` / `Text40`
- `Copy of ORDER` / `Text42`
- `Copy of ORDER` / `Text59`
- `Copy of ORDER` / `Text64`
- `Copy of ORDER` / `Text70`
- `Copy of ORDER` / `Text77`
- `Copy of ORDER` / `Text79`
- `Copy of ORDER` / `Text83`
- `Copy of ORDER` / `Text87`
- `Copy of ORDER` / `Text89`
- `Copy of ORDER` / `Text91`
- `Copy of ORDER` / `Text94`
- `Copy of ORDER` / `Text95`
- `Cust form` / `Box52`
- `Cust form` / `Label54`
- `Cust form` / `Label55`
- `Cust form` / `Label56`
- `Cust form` / `Label57`
- `Cust form` / `Label58`
- `Cust form` / `Text12`
- `Cust form` / `Text13`
- `Cust form` / `Text35`
- `Cust form` / `Text37`
- `Cust form` / `Text39`
- `Cust form` / `Text41`
- `Cust form` / `Text43`
- `Cust form` / `Text45`
- `Custnoteform` / `Label1`
- `Custnoteform` / `Label2`
- `Custnoteform` / `Label5`
- `Custnoteform` / `Label6`
- `Customer 2` / `Box52`
- `Customer 2` / `Label54`
- `Customer 2` / `Label55`
- `Customer 2` / `Label56`
- `Customer 2` / `Label57`
- `Customer 2` / `Label58`
- `Customer 2` / `Label60`
- `Customer 2` / `Label61`
- `Customer 2` / `Label63`
- `Customer 2` / `Label65`
- `Customer 2` / `Label67`
- `Customer 2` / `Text12`
- `Customer 2` / `Text13`
- `Customer 2` / `Text35`
- `Customer 2` / `Text37`
- `Customer 2` / `Text39`
- `Customer 2` / `Text41`
- `Customer 2` / `Text43`
- `Customer 2` / `Text45`
- `Customer 3` / `Box52`
- `Customer 3` / `Label158`
- `Customer 3` / `Label160`
- `Customer 3` / `Label54`
- `Customer 3` / `Label55`
- `Customer 3` / `Label56`
- `Customer 3` / `Label57`
- `Customer 3` / `Label58`
- `Customer 3` / `Text12`
- `Customer 3` / `Text13`
- `Customer 3` / `Text35`
- `Customer 3` / `Text37`
- `Customer 3` / `Text39`
- `Customer 3` / `Text41`
- `Customer 3` / `Text43`
- `Customer 3` / `Text45`
- `Customer` / `Box52`
- `Customer` / `Label54`
- `Customer` / `Label55`
- `Customer` / `Label56`
- `Customer` / `Label57`
- `Customer` / `Label58`
- `Customer` / `Label59`
- `Customer` / `Label61`
- `Customer` / `Label63`
- `Customer` / `Label65`
- `Customer` / `Label67`
- `Customer` / `Text12`
- `Customer` / `Text13`
- `Customer` / `Text35`
- `Customer` / `Text37`
- `Customer` / `Text39`
- `Customer` / `Text41`
- `Customer` / `Text43`
- `Customer` / `Text45`
- `DESCRIPTION` / `Text12`
- `DESCRIPTION` / `Text13`
- `DESCRIPTION` / `Text15`
- `DESCRIPTION` / `Text17`
- `Events To Do` / `Button39`
- `Events To Do` / `Text10`
- `Events To Do` / `Text12`
- `Events To Do` / `Text14`
- `Events To Do` / `Text16`
- `Events To Do` / `Text18`
- `Events To Do` / `Text20`
- `Events To Do` / `Text22`
- `Events To Do` / `Text24`
- `Events To Do` / `Text26`
- `Events To Do` / `Text28`
- `Events To Do` / `Text30`
- `Events To Do` / `Text33`
- `Events To Do` / `Text35`
- `Events To Do` / `Text36`
- `Events To Do` / `Text7`
- `Events To Do` / `Text8`
- `Events To Do` / `To Bill`
- `INVOICE EDIT FORM` / `Label125`
- `INVOICE EDIT FORM` / `Label126`
- `INVOICE EDIT FORM` / `Label127`
- `INVOICE EDIT FORM` / `Label132`
- `INVOICE EDIT FORM` / `Label14`
- `INVOICE EDIT FORM` / `Label15`
- `INVOICE EDIT FORM` / `Label20`
- `INVOICE EDIT FORM` / `Label28`
- `INVOICE EDIT FORM` / `Label29`
- `INVOICE EDIT FORM` / `Label31`
- `INVOICE EDIT FORM` / `Label59`
- `INVOICE EDIT FORM` / `Label74`
- `INVOICE EDIT FORM` / `Label75`
- `INVOICE EDIT FORM` / `Label76`
- `INVOICE EDIT FORM` / `Label77`
- `INVOICE EDIT FORM` / `Label86`
- `INVOICE EDIT FORM` / `Label93`
- `INVOICE EDIT FORM` / `ORDER_DETAIL_INVOICE2`
- `INVOICE EDIT FORM` / `Text117`
- `Invoice SwitchBoard1` / `Box71`
- `Invoice SwitchBoard1` / `Label18`
- `Invoice SwitchBoard1` / `Label35`
- `Invoice SwitchBoard1` / `Label36`
- `Invoice SwitchBoard1` / `Label37`
- `Invoice SwitchBoard1` / `Label38`
- `Invoice SwitchBoard1` / `Label72`
- `Invoice SwitchBoard1` / `Label73`
- `Invoice SwitchBoard1` / `Label75`
- `Invoice SwitchBoard1` / `Line39`
- `Invoice SwitchBoard1` / `Line48`
- `Invoice SwitchBoard1` / `Line64`
- `Invoice SwitchBoard1` / `Line65`
- `Invoice SwitchBoard1` / `Line66`
- `Invoice SwitchBoard1` / `Line67`
- `Invoice SwitchBoard1` / `Line68`
- `Invoice SwitchBoard1` / `Line69`
- `Invoice SwitchBoard1` / `Line70`
- `Invoice SwitchBoard1` / `Line74`
- `Invoice SwitchBoard1` / `Line76`
- `Invoice SwitchBoard1` / `Line80`
- `Invoice SwitchBoard2` / `Box71`
- `Invoice SwitchBoard2` / `Label18`
- `Invoice SwitchBoard2` / `Label35`
- `Invoice SwitchBoard2` / `Label36`
- `Invoice SwitchBoard2` / `Label37`
- `Invoice SwitchBoard2` / `Label38`
- `Invoice SwitchBoard2` / `Label72`
- `Invoice SwitchBoard2` / `Label73`
- `Invoice SwitchBoard2` / `Label75`
- `Invoice SwitchBoard2` / `Line39`
- `Invoice SwitchBoard2` / `Line48`
- `Invoice SwitchBoard2` / `Line64`
- `Invoice SwitchBoard2` / `Line65`
- `Invoice SwitchBoard2` / `Line66`
- `Invoice SwitchBoard2` / `Line67`
- `Invoice SwitchBoard2` / `Line68`
- `Invoice SwitchBoard2` / `Line69`
- `Invoice SwitchBoard2` / `Line70`
- `Invoice SwitchBoard2` / `Line74`
- `Invoice SwitchBoard2` / `Line76`
- `Invoice SwitchBoard2` / `Line80`
- `Invoice SwitchBoard` / `Box71`
- `Invoice SwitchBoard` / `Label18`
- `Invoice SwitchBoard` / `Label35`
- `Invoice SwitchBoard` / `Label36`
- `Invoice SwitchBoard` / `Label37`
- `Invoice SwitchBoard` / `Label38`
- `Invoice SwitchBoard` / `Label72`
- `Invoice SwitchBoard` / `Label73`
- `Invoice SwitchBoard` / `Label75`
- `Invoice SwitchBoard` / `Line39`
- `Invoice SwitchBoard` / `Line48`
- `Invoice SwitchBoard` / `Line64`
- `Invoice SwitchBoard` / `Line65`
- `Invoice SwitchBoard` / `Line66`
- `Invoice SwitchBoard` / `Line67`
- `Invoice SwitchBoard` / `Line68`
- `Invoice SwitchBoard` / `Line69`
- `Invoice SwitchBoard` / `Line70`
- `Invoice SwitchBoard` / `Line76`
- `Invoice SwitchBoard` / `Line80`
- `Job Note` / `Box52`
- `Job Note` / `Label54`
- `Job Note` / `Text12`
- `Job Note` / `Text13`
- `Job Note` / `Text35`
- `Job Note` / `Text37`
- `Job Note` / `Text39`
- `Job Note` / `Text41`
- `Job Note` / `Text43`
- `Job Note` / `Text45`
- `ORDER EDIT1` / `Box45`
- `ORDER EDIT1` / `Box60`
- `ORDER EDIT1` / `Evening`
- `ORDER EDIT1` / `ORDER_DETAIL`
- `ORDER EDIT1` / `Text105`
- `ORDER EDIT1` / `Text18`
- `ORDER EDIT1` / `Text34`
- `ORDER EDIT1` / `Text40`
- `ORDER EDIT1` / `Text42`
- `ORDER EDIT1` / `Text48`
- `ORDER EDIT1` / `Text59`
- `ORDER EDIT1` / `Text64`
- `ORDER EDIT1` / `Text68`
- `ORDER EDIT1` / `Text70`
- `ORDER EDIT1` / `Text77`
- `ORDER EDIT1` / `Text79`
- `ORDER EDIT1` / `Text83`
- `ORDER EDIT1` / `Text87`
- `ORDER EDIT1` / `Text89`
- `ORDER EDIT1` / `Text91`
- `ORDER EDIT1` / `Text94`
- `ORDER EDIT1` / `Text95`
- `ORDER EDIT` / `Box45`
- `ORDER EDIT` / `Box60`
- `ORDER EDIT` / `Evening`
- `ORDER EDIT` / `ORDER_DETAIL`
- `ORDER EDIT` / `Text105`
- `ORDER EDIT` / `Text18`
- `ORDER EDIT` / `Text34`
- `ORDER EDIT` / `Text40`
- `ORDER EDIT` / `Text42`
- `ORDER EDIT` / `Text48`
- `ORDER EDIT` / `Text59`
- `ORDER EDIT` / `Text64`
- `ORDER EDIT` / `Text68`
- `ORDER EDIT` / `Text70`
- `ORDER EDIT` / `Text77`
- `ORDER EDIT` / `Text79`
- `ORDER EDIT` / `Text83`
- `ORDER EDIT` / `Text87`
- `ORDER EDIT` / `Text89`
- `ORDER EDIT` / `Text91`
- `ORDER EDIT` / `Text94`
- `ORDER EDIT` / `Text95`
- `ORDER_DETAIL_INVOICE2` / `Line35`
- `ORDER_DETAIL_INVOICE2` / `Text10`
- `ORDER_DETAIL_INVOICE2` / `Text12`
- `ORDER_DETAIL_INVOICE2` / `Text23`
- `ORDER_DETAIL_INVOICE2` / `Text26`
- `ORDER_DETAIL_INVOICE2` / `Text8`
- `ORDER_DETAIL` / `Box36`
- `ORDER_DETAIL` / `Line35`
- `ORDER_DETAIL` / `Text10`
- `ORDER_DETAIL` / `Text12`
- `ORDER_DETAIL` / `Text23`
- `ORDER_DETAIL` / `Text26`
- `ORDER_DETAIL` / `Text8`
- `ORDER_DET_DISP_EVENT` / `T o Bill`
- `ORDER_DET_DISP_EVENT` / `Text13`
- `ORDER_DET_DISP_EVENT` / `Text15`
- `ORDER_DET_DISP_EVENT` / `Text21`
- `ORDER_DET_DISP_EVENT` / `Text25`
- `ORDER_DET_DISP_EVENT` / `Text44`
- `ORDER_DET_DISP_EVENT` / `Text45`
- `ORDER_DET_DISP_EVENT` / `Text46`
- `ORDER_DET_DISP_EVENT` / `Text53`
- `ORDER_DET_DISP_EVENT` / `Text55`
- `ORDER_DET_DISP_EVENT` / `Total Price`
- `ORDER_DET_DISP` / `Frequency`
- `ORDER_DET_DISP` / `ORDER_DET_DISP_EVENT`
- `ORDER_DET_DISP` / `Text15`
- `ORDER_DET_DISP` / `Text17`
- `ORDER_DET_DISP` / `Text19`
- `ORDER_DET_DISP` / `Text22`
- `ORDER_DET_DISP` / `Text25`
- `ORDER_DET_DISP` / `Text28`
- `ORDER` / `Box45`
- `ORDER` / `Box60`
- `ORDER` / `Evening`
- `ORDER` / `Frame128`
- `ORDER` / `Frame130`
- `ORDER` / `Frame134`
- `ORDER` / `Label129`
- `ORDER` / `Label131`
- `ORDER` / `Label132`
- `ORDER` / `Label135`
- `ORDER` / `Label139`
- `ORDER` / `Label141`
- `ORDER` / `Label152`
- `ORDER` / `Label156`
- `ORDER` / `Label157`
- `ORDER` / `Label158`
- `ORDER` / `Label160`
- `ORDER` / `Label161`
- `ORDER` / `Label177`
- `ORDER` / `Label179`
- `ORDER` / `Label183`
- `ORDER` / `Label184`
- `ORDER` / `Label185`
- `ORDER` / `Label186`
- `ORDER` / `Label187`
- `ORDER` / `Label188`
- `ORDER` / `Label189`
- `ORDER` / `Label190`
- `ORDER` / `Label191`
- `ORDER` / `Label192`
- `ORDER` / `Label194`
- `ORDER` / `Label196`
- `ORDER` / `Label198`
- `ORDER` / `Label200`
- `ORDER` / `Label202`
- `ORDER` / `Label204`
- `ORDER` / `Label206`
- `ORDER` / `Label208`
- `ORDER` / `Label210`
- `ORDER` / `Label212`
- `ORDER` / `Label214`
- `ORDER` / `Label216`
- `ORDER` / `Label218`
- `ORDER` / `Label220`
- `ORDER` / `Label222`
- `ORDER` / `Label224`
- `ORDER` / `Label226`
- `ORDER` / `Label228`
- `ORDER` / `Label230`
- `ORDER` / `Label232`
- `ORDER` / `Label234`
- `ORDER` / `Label236`
- `ORDER` / `Label243`
- `ORDER` / `Label246`
- `ORDER` / `ORDER_DETAIL`
- `ORDER` / `Text124`
- `ORDER` / `Text18`
- `ORDER` / `Text34`
- `ORDER` / `Text40`
- `ORDER` / `Text42`
- `ORDER` / `Text59`
- `ORDER` / `Text64`
- `ORDER` / `Text70`
- `ORDER` / `Text77`
- `ORDER` / `Text79`
- `ORDER` / `Text83`
- `ORDER` / `Text87`
- `ORDER` / `Text89`
- `ORDER` / `Text91`
- `ORDER` / `Text94`
- `ORDER` / `Text95`
- `OrderSwitchBoard` / `Label34`
- `OrderSwitchBoard` / `Label45`
- `OrderSwitchBoard` / `Label50`
- `OrderSwitchBoard` / `Label51`
- `OrderSwitchBoard` / `Label52`
- `OrderSwitchBoard` / `Label53`
- `OrderSwitchBoard` / `Label56`
- `Pest` / `Text10`
- `Pest` / `Text12`
- `Pest` / `Text7`
- `Pest` / `Text8`
- `Plant` / `Text10`
- `Plant` / `Text7`
- `Plant` / `Text8`
- `SpraySwitchBoard` / `Label54`
- `SpraySwitchBoard` / `Label55`
- `SpraySwitchBoard` / `Label56`
- `SpraySwitchBoard` / `Label58`
- `SpraySwitchBoard` / `Label59`
- `SpraySwitchBoard` / `Label60`
- `SpraySwitchBoard` / `Label63`
- `SpraySwitchBoard` / `Label70`
- `SpraySwitchBoard` / `Label72`
- `SpraySwitchBoard` / `Line51`
- `SpraySwitchBoard` / `Line52`
- `SpraySwitchBoard` / `Line53`
- `SpraySwitchBoard` / `OLEUnbound35`
- `SwitchBoard11` / `Button16`
- `SwitchBoard11` / `Text0`
- `SwitchBoard1` / `Label56`
- `SwitchBoard1` / `Label57`
- `SwitchBoard1` / `Label58`
- `SwitchBoard1` / `OLEUnbound38`
- `SwitchBoard1` / `OLEUnbound59`
- `SwitchBoard1` / `OLEUnbound60`
- `SwitchBoard1a` / `OLEUnbound38`
- `SwitchBoard2` / `Auto_Header0`
- `SwitchBoard` / `Text0`
- `SwitchboardAccountsReceivable` / `Label62`
- `SwitchboardAccountsReceivable` / `Label81`
- `SwitchboardAccountsReceivable` / `OLEUnbound38`
- `SwitchboardAccountsReceivable` / `OLEUnbound59`
- `SwitchboardAccountsReceivable` / `OLEUnbound60`
- `TOTALS` / `LAWN Label`
- `TOTALS` / `PERCENT GROWTH Label`
- `TOTALS` / `PPHM Label`
- `TOTALS` / `SPRAY Label`
- `TOTALS` / `WORKSHEETS Label`
- `TOTALS` / `YEAR Label`
- `TOTALS` / `YEARS GROSS Label`
- `Treatment Detail` / `Text18`
- `Treatment Detail` / `Text19`
- `Treatment Detail` / `Text20`
- `Treatment` / `Text12`
- `Treatment` / `Text13`
- `Treatment` / `Text15`
- `Treatment` / `Text23`
- `Treatment` / `Text26`
- `Treatment` / `Text28`
- `Treatment` / `Text30`
- `Treatment` / `Treatment Detail`
- `YEAR END SWITCHBOARD` / `Label13`
- `YEAR END SWITCHBOARD` / `Label14`
- `YEAR END SWITCHBOARD` / `Label15`
- `YEAR END SWITCHBOARD` / `Label16`
- `YEAR END SWITCHBOARD` / `Label18`
- `YEAR END SWITCHBOARD` / `Label30`
- `YEAR END SWITCHBOARD` / `Label31`
- `YEAR END SWITCHBOARD` / `Label32`
- `YEAR END SWITCHBOARD` / `Label33`
- `YEAR END SWITCHBOARD` / `Label35`
- `YEAR END SWITCHBOARD` / `Label36`
- `YEAR END SWITCHBOARD` / `Label37`
- `YEAR END SWITCHBOARD` / `Label38`
- `YEAR END SWITCHBOARD` / `Label39`
- `YEAR END SWITCHBOARD` / `Label40`
- `YEAR END SWITCHBOARD` / `Label52`
- `YEAR END SWITCHBOARD` / `Label53`
- `YEAR END SWITCHBOARD` / `Label55`
- `YEAR END SWITCHBOARD` / `Label56`
- `frmCrew2Sub` / `Label6`
- `frmCustomerFilterTest1` / `Label2`
- `frmCustomerFilterTest1` / `Label3`
- `frmCustomerFilterTest1` / `Label6`
- `frmCustomerFilterTest1` / `cmbCustomerLastName_Label`
- `frmCustomerFilterTest2` / `Label10`
- `frmCustomerFilterTest2` / `Label12`
- `frmCustomerFilterTest2` / `Label14`
- `frmCustomerFilterTest2` / `Label15`
- `frmCustomerFilterTest2` / `Label18`
- `frmCustomerFilterTest2` / `Label20`
- `frmCustomerFilterTest2` / `Label22`
- `frmCustomerFilterTest2` / `Label23`
- `frmCustomerFilterTest2` / `Label8`
- `frmCustomerFilterTest2` / `frmCustomerSubFormTest`
- `frmCustomerSubFormTest` / `Label0`
- `frmCustomerSubFormTest` / `Label1`
- `frmCustomerSubFormTest` / `Label2`
- `frmCustomerSubFormTest` / `Label3`
- `frmCustomerSubFormTest` / `Label4`
- `frmCustomerSubFormTest` / `Label5`
- `frmCustomerSubFormTest` / `Label6`
- `frmCustomerSubFormTest` / `Label7`
- `frmCustomerSubFormTest` / `Label8`
- `frmInvoiceGenerator` / `Label1`
- `frmInvoiceGenerator` / `Label3`
- `frmInvoiceGenerator` / `txtEndDate`
- `frmInvoiceGenerator` / `txtStartDate`
- `frmSuperScheduler` / `Crew 2 Total`
- `frmSuperScheduler` / `Image72`
- `frmSuperScheduler` / `Label100`
- `frmSuperScheduler` / `Label102`
- `frmSuperScheduler` / `Label105`
- `frmSuperScheduler` / `Label106`
- `frmSuperScheduler` / `Label107`
- `frmSuperScheduler` / `Label109`
- `frmSuperScheduler` / `Label10`
- `frmSuperScheduler` / `Label110`
- `frmSuperScheduler` / `Label112`
- `frmSuperScheduler` / `Label113`
- `frmSuperScheduler` / `Label12`
- `frmSuperScheduler` / `Label14`
- `frmSuperScheduler` / `Label16`
- `frmSuperScheduler` / `Label18`
- `frmSuperScheduler` / `Label22`
- `frmSuperScheduler` / `Label41`
- `frmSuperScheduler` / `Label42`
- `frmSuperScheduler` / `Label43`
- `frmSuperScheduler` / `Label44`
- `frmSuperScheduler` / `Label45`
- `frmSuperScheduler` / `Label51`
- `frmSuperScheduler` / `Label53`
- `frmSuperScheduler` / `Label54`
- `frmSuperScheduler` / `Label55`
- `frmSuperScheduler` / `Label56`
- `frmSuperScheduler` / `Label57`
- `frmSuperScheduler` / `Label58`
- `frmSuperScheduler` / `Label59`
- `frmSuperScheduler` / `Label60`
- `frmSuperScheduler` / `Label61`
- `frmSuperScheduler` / `Label62`
- `frmSuperScheduler` / `Label63`
- `frmSuperScheduler` / `Label65`
- `frmSuperScheduler` / `Label66`
- `frmSuperScheduler` / `Label74`
- `frmSuperScheduler` / `Label75`
- `frmSuperScheduler` / `Label83`
- `frmSuperScheduler` / `Label85`
- `frmSuperScheduler` / `Label87`
- `frmSuperScheduler` / `Label91`
- `frmSuperScheduler` / `Label96`
- `frmSuperScheduler` / `Label99`
- `frmSuperScheduler` / `Line78`
- `frmSuperScheduler` / `Line79`
- `frmSuperScheduler` / `Line80`
- `frmSuperScheduler` / `frmCrew1Sub Label`
- `frmSuperScheduler` / `frmCrew1Sub`
- `frmSuperScheduler` / `frmCrew2Sub Label`
- `frmSuperScheduler` / `frmCrew2Sub`
- `frmSuperScheduler` / `frmSuperSchedulerSub Label`
- `frmSuperScheduler` / `frmSuperSchedulerSub`
- `frmSuperScheduler` / `txtCrew1Total`
- `frmSuperScheduler` / `txtCrew2Total`
- `frmSuperScheduler` / `txtDailyTotal`
- `frmSuperScheduler` / `txtScheduleDate`
