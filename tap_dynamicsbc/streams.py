"""Stream type classes for tap-dynamicsbc."""

from __future__ import annotations

import typing as t
from importlib import resources

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_dynamicsbc.client import DynamicsBusinessCentralStream

SCHEMAS_DIR = resources.files(__package__) / "schemas"


class ClientsStream(DynamicsBusinessCentralStream):
    """Define clients stream."""

    name = "clients"
    path = "/apiCustomerCards"
    primary_keys: t.ClassVar[list[str]] = ["no"]
    replication_key = None
    records_jsonpath = "$.value[*]"

    def get_url_params(
        self,
        context: t.Any | None = None,  # noqa: ARG002
        next_page_token: t.Any | None = None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        params = super().get_url_params(context, next_page_token)
        params["$filter"] = "blocked eq ' '"
        return params
    
    schema = th.PropertiesList(
        th.Property("@odata.etag", th.StringType),
        th.Property("no", th.StringType, description="Customer number"),
        th.Property("address", th.StringType),
        th.Property("address2", th.StringType),
        th.Property("allowLineDisc", th.BooleanType),
        th.Property("amount", th.NumberType),
        th.Property("applicationMethod", th.StringType),
        th.Property("balance", th.NumberType),
        th.Property("balanceLCY", th.NumberType),
        th.Property("balanceDue", th.NumberType),
        th.Property("balanceDueLCY", th.NumberType),
        th.Property("baseCalendarCode", th.StringType),
        th.Property("billToCustomerNo", th.StringType),
        th.Property("billToNoOfArchivedDoc", th.IntegerType),
        th.Property("billToNoOfBlanketOrders", th.IntegerType),
        th.Property("billToNoOfCreditMemos", th.IntegerType),
        th.Property("billToNoOfInvoices", th.IntegerType),
        th.Property("billToNoOfOrders", th.IntegerType),
        th.Property("billToNoOfPstdCrMemos", th.IntegerType),
        th.Property("billToNoOfPstdInvoices", th.IntegerType),
        th.Property("billToNoOfPstdReturnR", th.IntegerType),
        th.Property("billToNoOfPstdShipments", th.IntegerType),
        th.Property("billToNoOfQuotes", th.IntegerType),
        th.Property("billToNoOfReturnOrders", th.IntegerType),
        th.Property("blockPaymentTolerance", th.BooleanType),
        th.Property("blocked", th.StringType),
        th.Property("budgetedAmount", th.NumberType),
        th.Property("cashFlowPaymentTermsCode", th.StringType),
        th.Property("categoryFNX", th.StringType),
        th.Property("ccmfnx", th.StringType),
        th.Property("chainName", th.StringType),
        th.Property("city", th.StringType),
        th.Property("cnpjcpffnx", th.StringType),
        th.Property("collectionMethod", th.StringType),
        th.Property("combineShipments", th.BooleanType),
        th.Property("comment", th.BooleanType),
        th.Property("companyNatureFNX", th.StringType),
        th.Property("contact", th.StringType),
        th.Property("contactGraphId", th.StringType),
        th.Property("contactID", th.StringType),
        th.Property("contactType", th.StringType),
        th.Property("contractGainLossAmount", th.NumberType),
        th.Property("copySellToAddrToQteFrom", th.StringType),
        th.Property("countryRegionCode", th.StringType),
        th.Property("county", th.StringType),
        th.Property("crMemoAmounts", th.NumberType),
    ).to_dict()


class ProductsStream(DynamicsBusinessCentralStream):
    """Define products stream."""

    name = "products"
    path = "/ItemCard"
    primary_keys: t.ClassVar[list[str]] = ["No"]
    replication_key = None
    records_jsonpath = "$.value[*]"
    
    schema = th.PropertiesList(
        th.Property("@odata.etag", th.StringType),
        th.Property("No", th.StringType, description="Product number"),
        th.Property("Description", th.StringType),
        th.Property("Description2FNX", th.StringType),
        th.Property("Description_2", th.StringType),
        th.Property("Blocked", th.BooleanType),
        th.Property("Type", th.StringType),
        th.Property("Base_Unit_of_Measure", th.StringType),
        th.Property("Last_Date_Modified", th.DateTimeType),
        th.Property("GTIN", th.StringType),
        th.Property("Item_Category_Code", th.StringType),
        th.Property("Manufacturer_Code", th.StringType),
        th.Property("Service_Item_Group", th.StringType),
        th.Property("Automatic_Ext_Texts", th.BooleanType),
        th.Property("Common_Item_No", th.StringType),
        th.Property("ManufacturerCodeFNX", th.StringType),
        th.Property("Purchasing_Code", th.StringType),
        th.Property("VariantMandatoryDefaultYes", th.StringType),
        th.Property("VariantMandatoryDefaultNo", th.StringType),
        th.Property("Product_Sale_Status", th.StringType),
        th.Property("Service_Transaction_Type_Code", th.StringType),
        th.Property("Exclude_From_Service_Decl", th.BooleanType),
        th.Property("Shelf_No", th.StringType),
        th.Property("Created_From_Nonstock_Item", th.BooleanType),
        th.Property("Search_Description", th.StringType),
        th.Property("Inventory", th.NumberType),
        th.Property("InventoryNonFoundation", th.NumberType),
        th.Property("Qty_on_Purch_Order", th.NumberType),
        th.Property("Qty_on_Prod_Order", th.NumberType),
        th.Property("Qty_on_Component_Lines", th.NumberType),
        th.Property("Qty_on_Sales_Order", th.NumberType),
        th.Property("Qty_Tracking", th.NumberType),
        th.Property("Qty_on_Service_Order", th.NumberType),
        th.Property("Qty_on_Job_Order", th.NumberType),
        th.Property("Qty_on_Assembly_Order", th.NumberType),
        th.Property("Qty_on_Asm_Component", th.NumberType),
        th.Property("StockoutWarningDefaultYes", th.StringType),
        th.Property("StockoutWarningDefaultNo", th.StringType),
        th.Property("PreventNegInventoryDefaultYes", th.StringType),
        th.Property("PreventNegInventoryDefaultNo", th.StringType),
        th.Property("Net_Weight", th.NumberType),
        th.Property("Gross_Weight", th.NumberType),
        th.Property("Unit_Volume", th.NumberType),
        th.Property("Over_Receipt_Code", th.StringType),
        th.Property("Trans_Ord_Receipt_Qty", th.NumberType),
        th.Property("Trans_Ord_Shipment_Qty", th.NumberType),
        th.Property("Qty_in_Transit", th.NumberType),
        th.Property("Costing_Method", th.StringType),
        th.Property("Standard_Cost", th.NumberType),
        th.Property("Unit_Cost", th.NumberType),
        th.Property("Indirect_Cost_Percent", th.NumberType),
        th.Property("Last_Direct_Cost", th.NumberType),
        th.Property("Net_Invoiced_Qty", th.NumberType),
        th.Property("Cost_is_Adjusted", th.BooleanType),
        th.Property("Excluded_from_Cost_Adjustment", th.BooleanType),
        th.Property("Cost_is_Posted_to_G_L", th.BooleanType),
        th.Property("Inventory_Value_Zero", th.BooleanType),
        th.Property("SpecialPurchPriceListTxt", th.StringType),
        th.Property("SpecialPurchPricesAndDiscountsTxt", th.StringType),
        th.Property("Gen_Prod_Posting_Group", th.StringType),
        th.Property("VAT_Prod_Posting_Group", th.StringType),
        th.Property("Tax_Group_Code", th.StringType),
        th.Property("Inventory_Posting_Group", th.StringType),
        th.Property("Default_Deferral_Template_Code", th.StringType),
        th.Property("Tariff_No", th.StringType),
        th.Property("Country_Region_of_Origin_Code", th.StringType),
        th.Property("Exclude_from_Intrastat_Report", th.BooleanType),
        th.Property("Supplementary_Unit_of_Measure", th.StringType),
        th.Property("Unit_Price", th.NumberType),
        th.Property("CalcUnitPriceExclVAT", th.NumberType),
        th.Property("Price_Includes_VAT", th.BooleanType),
        th.Property("Price_Profit_Calculation", th.StringType),
        th.Property("Profit_Percent", th.NumberType),
        th.Property("SpecialSalesPriceListTxt", th.StringType),
        th.Property("SpecialPricesAndDiscountsTxt", th.StringType),
        th.Property("Allow_Invoice_Disc", th.BooleanType),
        th.Property("Item_Disc_Group", th.StringType),
        th.Property("Sales_Unit_of_Measure", th.StringType),
        th.Property("Service_Commitment_Option", th.StringType),
        th.Property("Sales_Blocked", th.BooleanType),
        th.Property("Service_Blocked", th.BooleanType),
        th.Property("Application_Wksh_User_ID", th.StringType),
        th.Property("VAT_Bus_Posting_Gr_Price", th.StringType),
        th.Property("Replenishment_System", th.StringType),
        th.Property("Lead_Time_Calculation", th.StringType),
        th.Property("Vendor_No", th.StringType),
        th.Property("Vendor_Item_No", th.StringType),
        th.Property("Purch_Unit_of_Measure", th.StringType),
        th.Property("Purchasing_Blocked", th.BooleanType),
        th.Property("UsageDataSupplierRefExists", th.BooleanType),
        th.Property("Manufacturing_Policy", th.StringType),
        th.Property("Routing_No", th.StringType),
        th.Property("Production_BOM_No", th.StringType),
        th.Property("Rounding_Precision", th.NumberType),
        th.Property("Flushing_Method", th.StringType),
        th.Property("Overhead_Rate", th.NumberType),
        th.Property("Scrap_Percent", th.NumberType),
        th.Property("Lot_Size", th.NumberType),
        th.Property("Allow_Whse_Overpick", th.BooleanType),
        th.Property("Production_Blocked", th.StringType),
        th.Property("Assembly_Policy", th.StringType),
        th.Property("AssemblyBOM", th.BooleanType),
        th.Property("Reordering_Policy", th.StringType),
        th.Property("Reserve", th.StringType),
        th.Property("Order_Tracking_Policy", th.StringType),
        th.Property("Stockkeeping_Unit_Exists", th.BooleanType),
        th.Property("Dampener_Period", th.StringType),
        th.Property("Dampener_Quantity", th.NumberType),
        th.Property("Critical", th.BooleanType),
        th.Property("Safety_Lead_Time", th.StringType),
        th.Property("Safety_Stock_Quantity", th.NumberType),
        th.Property("Include_Inventory", th.BooleanType),
        th.Property("Lot_Accumulation_Period", th.StringType),
        th.Property("Rescheduling_Period", th.StringType),
        th.Property("Reorder_Point", th.NumberType),
        th.Property("Reorder_Quantity", th.NumberType),
        th.Property("Maximum_Inventory", th.NumberType),
        th.Property("Overflow_Level", th.NumberType),
        th.Property("Time_Bucket", th.StringType),
        th.Property("Minimum_Order_Quantity", th.NumberType),
        th.Property("Maximum_Order_Quantity", th.NumberType),
        th.Property("Order_Multiple", th.NumberType),
        th.Property("Item_Tracking_Code", th.StringType),
        th.Property("Serial_Nos", th.StringType),
        th.Property("Lot_Nos", th.StringType),
        th.Property("Expiration_Calculation", th.StringType),
        th.Property("Acceptable_Percent", th.NumberType),
        th.Property("Warehouse_Class_Code", th.StringType),
        th.Property("Special_Equipment_Code", th.StringType),
        th.Property("Put_away_Template_Code", th.StringType),
        th.Property("Put_away_Unit_of_Measure_Code", th.StringType),
        th.Property("Phys_Invt_Counting_Period_Code", th.StringType),
        th.Property("Last_Phys_Invt_Date", th.DateTimeType),
        th.Property("Last_Counting_Period_Update", th.DateTimeType),
        th.Property("Next_Counting_Start_Date", th.DateTimeType),
        th.Property("Next_Counting_End_Date", th.DateTimeType),
        th.Property("Identifier_Code", th.StringType),
        th.Property("Use_Cross_Docking", th.BooleanType),
        th.Property("ServiceCodeFNX", th.StringType),
        th.Property("FixedAssetNoFNX", th.StringType),
        th.Property("NCMCodeFNX", th.StringType),
        th.Property("NCMExceptionCodeFNX", th.StringType),
        th.Property("CESTCodeFNX", th.StringType),
        th.Property("HasGTINFNX", th.BooleanType),
        th.Property("GTINFNX", th.StringType),
        th.Property("ANPCodeFNX", th.StringType),
        th.Property("ANVISACodeFNX", th.StringType),
        th.Property("OriginCodeFNX", th.StringType),
        th.Property("TaxExceptionCodeFNX", th.StringType),
        th.Property("NetWeightFNX", th.NumberType),
        th.Property("GrossWeightFNX", th.NumberType),
        th.Property("ICMS60RetSTBaseAmount_PTE", th.NumberType),
        th.Property("ICMS60RetSTAmount_PTE", th.NumberType),
        th.Property("ICMS60STPercent_PTE", th.NumberType),
        th.Property("ICMS60SubstituteICMSAmount_PTE", th.NumberType),
        th.Property("GHG_Credit", th.BooleanType),
        th.Property("Carbon_Credit_Per_UOM", th.NumberType),
        th.Property("Sust_Cert_No", th.StringType),
        th.Property("Sust_Cert_Name", th.StringType),
        th.Property("Default_Sust_Account", th.StringType),
        th.Property("Default_CO2_Emission", th.NumberType),
        th.Property("Default_CH4_Emission", th.NumberType),
        th.Property("Default_N2O_Emission", th.NumberType),
        th.Property("CO2e_per_Unit", th.NumberType),
        th.Property("Global_Dimension_1_Filter", th.StringType),
        th.Property("Global_Dimension_2_Filter", th.StringType),
        th.Property("Location_Filter", th.StringType),
        th.Property("Drop_Shipment_Filter", th.StringType),
        th.Property("Variant_Filter", th.StringType),
        th.Property("Lot_No_Filter", th.StringType),
        th.Property("Serial_No_Filter", th.StringType),
        th.Property("Unit_of_Measure_Filter", th.StringType),
        th.Property("Package_No_Filter", th.StringType),
        th.Property("Date_Filter", th.StringType),
    ).to_dict()


class PricesStream(DynamicsBusinessCentralStream):
    """Define prices stream."""

    name = "prices"
    path = "/itemprice"
    primary_keys: t.ClassVar[list[str]] = ["Price_List_Code", "Line_No"]
    replication_key = None
    records_jsonpath = "$.value[*]"
    
    def get_url_params(
        self,
        context: t.Any | None = None,  # noqa: ARG002
        next_page_token: t.Any | None = None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        params = super().get_url_params(context, next_page_token)
        params["$filter"] = "Price_List_Code eq '01'"
        return params
    
    schema = th.PropertiesList(
        th.Property("@odata.etag", th.StringType),
        th.Property("Price_List_Code", th.StringType, description="Price list code"),
        th.Property("Line_No", th.IntegerType, description="Line number"),
        th.Property("PriceListDescription", th.StringType, description="Price list description"),
        th.Property("Status", th.StringType),
        th.Property("Source_Type", th.StringType),
        th.Property("Source_No", th.StringType),
        th.Property("Asset_Type", th.StringType),
        th.Property("Asset_No", th.StringType, description="Asset number (Item number)"),
        th.Property("Description", th.StringType, description="Item description"),
        th.Property("Variant_Code", th.StringType),
        th.Property("Work_Type_Code", th.StringType),
        th.Property("Unit_of_Measure_Code", th.StringType),
        th.Property("Minimum_Quantity", th.NumberType),
        th.Property("Amount_Type", th.StringType),
        th.Property("Currency_Code", th.StringType),
        th.Property("Unit_Price", th.NumberType, description="Unit price"),
        th.Property("Cost_Factor", th.NumberType),
        th.Property("DirectUnitCost", th.NumberType),
        th.Property("Unit_Cost", th.NumberType),
        th.Property("Starting_Date", th.StringType),
        th.Property("Ending_Date", th.StringType),
        th.Property("Allow_Line_Disc", th.BooleanType),
        th.Property("Line_Discount_Percent", th.NumberType),
        th.Property("PurchLineDiscountPct", th.NumberType),
        th.Property("Allow_Invoice_Disc", th.BooleanType),
    ).to_dict()