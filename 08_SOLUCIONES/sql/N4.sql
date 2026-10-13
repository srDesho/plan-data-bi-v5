SELECT COUNT(DISTINCT cliente_id) planificados,COUNT(DISTINCT CASE WHEN realizada=1 THEN cliente_id END) visitados FROM visitas WHERE planificada=1;
