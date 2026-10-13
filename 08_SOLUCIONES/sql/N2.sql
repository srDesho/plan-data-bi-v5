SELECT COUNT(*) planificadas,SUM(realizada) realizadas,ROUND(100.0*SUM(realizada)/COUNT(*),2) cobertura FROM visitas WHERE planificada=1;
