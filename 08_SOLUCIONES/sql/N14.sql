SELECT cliente_id,ruta,COALESCE(zona,'Sin zona') zona,CASE WHEN zona IS NULL THEN 'Revisar' ELSE 'Completo' END estado_calidad FROM clientes ORDER BY cliente_id;
