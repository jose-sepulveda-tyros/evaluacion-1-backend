```text
OK 01. Estudiantes inicialmente vacíos — HTTP 200
OK 02. Salas inicialmente vacías — HTTP 200
OK 03. Reservas inicialmente vacías — HTTP 200
OK 04. Incidencias inicialmente vacías — HTTP 200
OK 05. Crear estudiante — HTTP 201
OK 06. Crear segundo estudiante — HTTP 201
OK 07. Consultar estudiante — HTTP 200
OK 08. Listar estudiantes — HTTP 200
OK 09. Crear sala con equipamiento como lista — HTTP 201
OK 10. Crear segunda sala — HTTP 201
OK 11. Consultar sala — HTTP 200
OK 12. Listar salas — HTTP 200
OK 13. Actualizar sala sin reservas — HTTP 200
OK 14. Crear reserva válida — HTTP 201
OK 15. Crear segunda reserva contigua — HTTP 201
OK 16. Otro estudiante y horario contiguo anterior — HTTP 201
OK 17. Consultar reserva — HTTP 200
OK 18. Superposición — HTTP 409
OK 19. Tercera reserva activa diaria — HTTP 400
OK 20. Cancelada no ocupa horario ni consume cupo — HTTP 201
OK 21. Filtrar, ordenar y paginar con varios resultados — HTTP 200
OK 22. Combinar los cuatro filtros — HTTP 200
OK 23. Página fuera de rango conserva metadatos — HTTP 200
OK 24. Filtro sin coincidencias — HTTP 200
OK 25. Sala inexistente — HTTP 404
OK 26. Estudiante inexistente — HTTP 404
OK 27. Horario invertido — HTTP 400
OK 28. Horario de duración cero — HTTP 400
OK 29. Exceso de capacidad — HTTP 400
OK 30. Longitud mínima — HTTP 422
OK 31. Correo inválido — HTTP 422
OK 32. Cantidad no positiva — HTTP 422
OK 33. Estado fuera del conjunto permitido — HTTP 422
OK 34. Fecha imposible — HTTP 422
OK 35. Consulta inválida: pagina=0 — HTTP 422
OK 36. Consulta inválida: limite=101 — HTTP 422
OK 37. Consulta inválida: direccion=otro — HTTP 422
OK 38. Consulta inválida: ordenar_por=correo — HTTP 422
OK 39. Actualizar reserva con PUT completo — HTTP 200
OK 40. PUT incompleto — HTTP 422
OK 41. PUT con horario inválido — HTTP 400
OK 42. Rechazos no alteran reserva — HTTP 200
OK 43. Reactivación superpuesta — HTTP 409
OK 44. Reducir capacidad incompatible — HTTP 409
OK 45. Capacidad original conservada — HTTP 200
OK 46. Cancelar libera cupo diario — HTTP 200
OK 47. Crear tras liberar cupo — HTTP 201
OK 48. Reactivar supera límite diario — HTTP 400
OK 49. Registrar incidencia — HTTP 201
OK 50. Incidencia para sala inexistente — HTTP 404
OK 51. Listar incidencias — HTTP 200
OK 52. Resolver incidencia — HTTP 200
OK 53. Reabrir incidencia — HTTP 200
OK 54. Incidencia inexistente — HTTP 404
OK 55. Incidencia rechaza otros campos — HTTP 422
OK 56. Estudiante inexistente en consulta — HTTP 404
OK 57. Sala inexistente en consulta — HTTP 404
OK 58. ID de reserva inválido — HTTP 422
OK 59. Eliminar reserva sin cuerpo — HTTP 204
OK 60. Consultar reserva eliminada — HTTP 404
OK 61. Eliminar nuevamente — HTTP 404
OK 62. Reactivar después de eliminar — HTTP 200
OK 63. Estado final de la colección — HTTP 200
Resultado: 63 casos correctos; 15 operaciones cubiertas.
```