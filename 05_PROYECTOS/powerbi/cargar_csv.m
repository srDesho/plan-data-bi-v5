// Crea una consulta en blanco, pega este ejemplo y ajusta la ruta local.
let
    Source = Csv.Document(File.Contents("C:\Plan_Data_BI_v5_Completo\05_PROYECTOS\powerbi\datos_modelo\fact_ventas.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers,{{"item_id",Int64.Type},{"pedido_id",Int64.Type},{"cantidad",Int64.Type},{"monto_centavos",Int64.Type},{"fecha_id",Int64.Type},{"estado",type text},{"ruta",type text},{"mes",type text}})
in
    Typed
