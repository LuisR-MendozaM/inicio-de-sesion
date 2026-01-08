# import flet as ft
# import threading
# import time
# import datetime
# import json
# import os
# import random
# from cajaAzul import BlueBox
# from configuracion import ConfiguracionContainer
# from excel5 import ExcelUnicoArchivo
# from alertas import SistemaAlertas, AlertasView
# from paguina1 import UMA

# class RelojGlobal:
#     def __init__(self):
#         self.horas_registradas = []
#         self.archivo_horas = "horas.json"
#         self.historial_registros = []
#         self.archivo_historial = "historial_registros.json"
#         self.reloj_activo = True
#         self.ultima_ejecucion = {}
#         self.callbacks = []
#         self.historial_callbacks = []
        
#         # Cargar horas guardadas
#         self.cargar_horas()
#         self.cargar_historial()
#         self.iniciar()

#     def agregar_callback(self, callback):
#         """Agrega una función que se ejecutará cuando suene una alarma"""
#         self.callbacks.append(callback)
    
#     def agregar_callback_historial(self, callback):
#         """Agrega una función que se ejecutará cuando se agregue un nuevo registro al historial"""
#         self.historial_callbacks.append(callback)

#     def cargar_horas(self):
#         """Carga las horas desde archivo JSON"""
#         if os.path.exists(self.archivo_horas):
#             try:
#                 with open(self.archivo_horas, "r") as file:
#                     datos = json.load(file)
#                     self.horas_registradas = [
#                         datetime.datetime.strptime(h, "%H:%M").time()
#                         for h in datos
#                     ]
#                 print(f"RelojGlobal: Horas cargadas: {[h.strftime('%I:%M %p') for h in self.horas_registradas]}")
#             except Exception as e:
#                 print(f"RelojGlobal: Error cargando horas: {e}")
#                 self.horas_registradas = []
    
#     def cargar_historial(self):
#         """Carga el historial desde archivo JSON"""
#         if os.path.exists(self.archivo_historial):
#             try:
#                 with open(self.archivo_historial, "r") as file:
#                     self.historial_registros = json.load(file)
#                 print(f"RelojGlobal: Historial cargado ({len(self.historial_registros)} registros)")
#             except Exception as e:
#                 print(f"RelojGlobal: Error cargando historial: {e}")
#                 self.historial_registros = []
#         else:
#             self.guardar_historial()

#     def guardar_horas(self):
#         """Guarda las horas en archivo JSON"""
#         try:
#             datos = [h.strftime("%H:%M") for h in self.horas_registradas]
#             with open(self.archivo_horas, "w") as file:
#                 json.dump(datos, file)
#         except Exception as e:
#             print(f"RelojGlobal: Error guardando horas: {e}")
    
#     def guardar_historial(self):
#         """Guarda el historial en archivo JSON"""
#         try:
#             if len(self.historial_registros) > 50:
#                 self.historial_registros = self.historial_registros[-50:]
            
#             with open(self.archivo_historial, "w") as file:
#                 json.dump(self.historial_registros, file, indent=2)
#         except Exception as e:
#             print(f"RelojGlobal: Error guardando historial: {e}")

#     def agregar_hora(self, hora_time):
#         """Agrega una hora a la lista global"""
#         if hora_time not in self.horas_registradas:
#             self.horas_registradas.append(hora_time)
#             self.guardar_horas()
#             print(f"RelojGlobal: Hora agregada: {hora_time.strftime('%I:%M %p')}")
#             return True
#         return False

#     def eliminar_hora(self, hora_time):
#         """Elimina una hora de la lista global"""
#         if hora_time in self.horas_registradas:
#             self.horas_registradas.remove(hora_time)
#             self.guardar_horas()
#             print(f"RelojGlobal: Hora eliminada: {hora_time.strftime('%I:%M %p')}")
#             return True
#         return False
    
#     def agregar_al_historial(self, datos, tipo="registro_automatico", fuente="Reloj Global"):
#         """Agrega un registro al historial"""
#         registro = {
#             "fecha": datetime.datetime.now().strftime("%d/%m/%y"),
#             "hora": datetime.datetime.now().strftime("%H:%M"),
#             "datos": datos,
#             "tipo": tipo,
#             "fuente": fuente
#         }
#         self.historial_registros.append(registro)
#         self.guardar_historial()
        
#         # Notificar a todos los callbacks
#         for callback in self.historial_callbacks:
#             try:
#                 callback()
#             except Exception as e:
#                 print(f"RelojGlobal: Error en callback de historial: {e}")
        
#         return registro
    
#     def limpiar_historial(self):
#         """Limpia todo el historial"""
#         self.historial_registros = []
#         self.guardar_historial()
#         print("RelojGlobal: Historial limpiado")
        
#         # Notificar a los callbacks
#         for callback in self.historial_callbacks:
#             try:
#                 callback()
#             except Exception as e:
#                 print(f"RelojGlobal: Error en callback de limpieza: {e}")

#     def iniciar(self):
#         """Inicia el reloj global en un hilo separado"""
#         if not hasattr(self, 'thread') or not self.thread.is_alive():
#             self.thread = threading.Thread(target=self._loop, daemon=True)
#             self.thread.start()
#             print("RelojGlobal: Iniciado")

#     def _loop(self):
#         """Loop principal del reloj"""
#         while self.reloj_activo:
#             try:
#                 ahora = datetime.datetime.now()
                
#                 for hora_obj in self.horas_registradas:
#                     hora_actual_minuto = ahora.strftime("%I:%M %p")
#                     segundos = ahora.strftime("%S")
#                     hora_objetivo_str = hora_obj.strftime("%I:%M %p")

#                     if hora_actual_minuto == hora_objetivo_str and segundos == "00":
#                         h_obj = datetime.datetime.combine(ahora.date(), hora_obj)
#                         clave = h_obj.strftime("%Y-%m-%d %H:%M")

#                         if clave not in self.ultima_ejecucion:
#                             self.ultima_ejecucion[clave] = True
#                             self._ejecutar_alarma(hora_objetivo_str)
#                             print(f"RelojGlobal: ✓ Alarma: {hora_objetivo_str}")
                
#                 hoy = datetime.datetime.now().date()
#                 claves_a_eliminar = [k for k in self.ultima_ejecucion 
#                                     if datetime.datetime.strptime(k.split(" ")[0], "%Y-%m-%d").date() < hoy]
#                 for k in claves_a_eliminar:
#                     del self.ultima_ejecucion[k]

#                 time.sleep(1)
                
#             except Exception as e:
#                 print(f"RelojGlobal: Error en loop: {e}")
#                 time.sleep(1)

#     def _ejecutar_alarma(self, hora):
#         """Ejecuta todos los callbacks registrados"""
#         for callback in self.callbacks:
#             try:
#                 callback(hora)
#             except Exception as e:
#                 print(f"RelojGlobal: Error en callback: {e}")

#     def detener(self):
#         """Detiene el reloj global"""
#         self.reloj_activo = False


# class UI(ft.Container):
#     def __init__(self, page):
#         super().__init__(expand=True)
#         self.page = page
        
#         # COLORES PARA LA BARRA DE NAVEGACIÓN
#         self.color_primario = "#27F5B4"  # Verde agua
#         self.color_fondo = "#FFFFFF"  # Blanco
#         self.color_texto = "#2C3E50"  # Azul oscuro
#         self.color_texto_secundario = "#6C757D"  # Gris
#         self.color_borde = "#E9ECEF"  # Gris claro para bordes
        
#         # Datos en tiempo real (manteniendo los originales)
#         self.datos_tiempo_real = {
#             'temperatura': 0,
#             'humedad': 0, 
#             'presion1': 0,
#             'presion2': 0,
#             'presion3': 0,
#         }

#         self.excel_manager = ExcelUnicoArchivo()
#         self.bandera_excel = self.excel_manager.get_bandera_archivo()
        
#         self.reloj_global = RelojGlobal()
#         self.sistema_alertas = SistemaAlertas()
#         self.alertas_view = None
        
#         # Variable para el badge de notificaciones
#         self.notificacion_badge = None
#         # Variable para saber si estamos en la página de Alertas
#         self.en_pagina_alertas = False

#         self.banner = ft.Banner(
#             bgcolor=ft.Colors.AMBER_100,
#             leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
#             content=ft.Text(
#                 "Sistema de monitoreo iniciado",
#                 color=ft.Colors.BLACK,
#             ),
#             actions=[
#                 ft.TextButton("OK", on_click=self.cerrar_banner)
#             ],
#         )
#         self.page.controls.append(self.banner)

#         if not self.bandera_excel:
#             print("⚠️ Main: No se encontró archivo Excel, mostrando banner...")
#             self.mostrar_banner_inicio()
#         else:
#             self.reloj_global.agregar_callback(self._on_alarma)
#             print("✅ Main: Archivo Excel encontrado")

#         self.color_teal = ft.Colors.GREY_300

#         self._initialize_ui_components()
#         self.content = self.resp_container
        
#         self.inicializar_alertas_view()

#     # def _crear_boton_navegacion_profesional(self, texto, icono, index):
#     #     """Crea un botón de navegación con diseño profesional y badge de notificaciones"""
#     #     # Contador de notificaciones (solo para el botón de Alertas)
#     #     if index == 2:  # Botón de Alertas
#     #         badge = ft.Container(
#     #             width=20,
#     #             height=20,
#     #             bgcolor=ft.Colors.RED_600,
#     #             border_radius=10,
#     #             alignment=ft.alignment.center,
#     #             visible=False,  # Inicialmente oculto
#     #             content=ft.Text(
#     #                 "0",
#     #                 size=10,
#     #                 color=ft.Colors.WHITE,
#     #                 weight=ft.FontWeight.BOLD
#     #             )
#     #         )
#     #         # Guardar referencia al badge
#     #         self.notificacion_badge = badge
#     #     else:
#     #         badge = ft.Container()  # Contenedor vacío para otros botones
        
#     #     return ft.Container(
#     #         width=160,
#     #         height=60,
#     #         bgcolor=ft.Colors.WHITE,
#     #         border_radius=10,
#     #         border=ft.border.all(1, self.color_borde),
#     #         alignment=ft.alignment.center,
#     #         clip_behavior=ft.ClipBehavior.HARD_EDGE,
#     #         animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
#     #         on_hover=lambda e: self._on_hover_boton_nav(e, index),
#     #         on_click=lambda e: self.change_page_manual(index),
#     #         content=ft.Stack(
#     #             controls=[
#     #                 ft.Row(
#     #                     alignment=ft.MainAxisAlignment.CENTER,
#     #                     vertical_alignment=ft.CrossAxisAlignment.CENTER,
#     #                     spacing=15,
#     #                     controls=[
#     #                         ft.Icon(icono, color=self.color_texto_secundario, size=22),
#     #                         ft.Text(
#     #                             texto, 
#     #                             color=self.color_texto,
#     #                             weight=ft.FontWeight.W_600,
#     #                             size=14
#     #                         )
#     #                     ]
#     #                 ),
#     #                 # Badge de notificaciones en la esquina superior derecha
#     #                 # ft.Container(
#     #                 #     top=5,
#     #                 #     right=10,
#     #                 #     content=badge
#     #                 # )
#     #                 ft.Container(
#     #                     alignment=ft.alignment.top_right,
#     #                     margin=ft.margin.only(right=5, top=5),
#     #                     content=badge
#     #                 )

#     #             ]
#     #         )
#     #     )

#     # def _on_hover_boton_nav(self, e, index):
#     #     """Maneja el hover de los botones de navegación"""
#     #     ctrl = e.control
#     #     is_hover = (e.data == "true" or e.data is True)
        
#     #     # Determinar qué botón está activo
#     #     botones = [self.btn_connect, self.btn_connect2, self.btn_connect3, self.btn_connect4]
#     #     index_activo = self.container_list_1.index(self.container_1.content) if self.container_1.content in self.container_list_1 else 0
        
#     #     # Si no es el botón activo
#     #     if index != index_activo:
#     #         if is_hover:
#     #             ctrl.bgcolor = f"{self.color_primario}10"  # 10% de opacidad
#     #             ctrl.border = ft.border.all(1, self.color_primario)
#     #             ctrl.scale = ft.Scale(1.02)
#     #             # Cambiar color del icono y texto
#     #             if len(ctrl.content.controls[0].controls) > 0:
#     #                 row_controls = ctrl.content.controls[0].controls
#     #                 if hasattr(row_controls[0], 'color'):
#     #                     row_controls[0].color = self.color_primario
#     #                 if hasattr(row_controls[1], 'color'):
#     #                     row_controls[1].color = self.color_primario
#     #         else:
#     #             ctrl.bgcolor = ft.Colors.WHITE
#     #             ctrl.border = ft.border.all(1, self.color_borde)
#     #             ctrl.scale = ft.Scale(1.0)
#     #             # Volver a colores normales
#     #             if len(ctrl.content.controls[0].controls) > 0:
#     #                 row_controls = ctrl.content.controls[0].controls
#     #                 if hasattr(row_controls[0], 'color'):
#     #                     row_controls[0].color = self.color_texto_secundario
#     #                 if hasattr(row_controls[1], 'color'):
#     #                     row_controls[1].color = self.color_texto
        
#     #     # Usar try-except para evitar errores si la página no está lista
#     #     try:
#     #         ctrl.update()
#     #     except:
#     #         pass    

#     def _crear_boton_navegacion_profesional(self, texto, icono, index):
#         """Crea un botón de navegación con diseño profesional y badge de notificaciones"""
        
#         # Contenedor para el contenido del botón (icono + texto)
#         contenido_boton = ft.Row(
#             alignment=ft.MainAxisAlignment.CENTER,
#             vertical_alignment=ft.CrossAxisAlignment.CENTER,
#             spacing=15,
#             controls=[
#                 ft.Icon(icono, color=self.color_texto_secundario, size=22),
#                 ft.Text(
#                     texto, 
#                     color=self.color_texto,
#                     weight=ft.FontWeight.W_600,
#                     size=14
#                 )
#             ]
#         )
        
#         # Crear el botón principal
#         boton_principal = ft.Container(
#             width=160,
#             height=60,
#             bgcolor=ft.Colors.WHITE,
#             border_radius=10,
#             border=ft.border.all(1, self.color_borde),
#             alignment=ft.alignment.center,
#             clip_behavior=ft.ClipBehavior.HARD_EDGE,
#             animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
#             on_hover=lambda e: self._on_hover_boton_nav(e, index),
#             on_click=lambda e: self.change_page_manual(index),
#         )
        
#         # Si es el botón de Alertas, agregar el badge
#         if index == 2:
#             # Crear el badge
#             badge = ft.Container(
#                 width=20,
#                 height=20,
#                 border_radius=10,
#                 bgcolor=ft.Colors.RED_600,
#                 alignment=ft.alignment.center,
#                 visible=False,
#                 content=ft.Text(
#                     "0",
#                     size=10,
#                     color=ft.Colors.WHITE,
#                     weight=ft.FontWeight.BOLD
#                 )
#             )
            
#             # Guardar referencia al badge
#             self.notificacion_badge = badge
            
#             # Crear el Stack con el botón y el badge
#             stack_content = ft.Stack(
#                 controls=[
#                     # El contenido del botón (centrado)
#                     ft.Container(
#                         content=contenido_boton,
#                         alignment=ft.alignment.center,
#                         width=160,
#                         height=60,
#                     ),
#                     # El badge posicionado en la esquina superior derecha
#                     badge
#                 ],
#                 width=170,  # Un poco más ancho para el badge
#                 height=65,  # Un poco más alto para el badge
#             )
            
#             # Configurar el badge para que esté en la esquina superior derecha
#             badge.top = 0
#             badge.right = 0
            
#             boton_principal.content = stack_content
#             return boton_principal
#         else:
#             # Para otros botones, contenido simple
#             boton_principal.content = contenido_boton
#             return boton_principal

#     def _on_hover_boton_nav(self, e, index):
#         """Maneja el hover de los botones de navegación"""
#         ctrl = e.control
#         is_hover = (e.data == "true" or e.data is True)
        
#         # Determinar qué botón está activo
#         botones = [self.btn_connect, self.btn_connect2, self.btn_connect3, self.btn_connect4]
#         index_activo = self.container_list_1.index(self.container_1.content) if self.container_1.content in self.container_list_1 else 0
        
#         # Si no es el botón activo
#         if index != index_activo:
#             if is_hover:
#                 ctrl.bgcolor = f"{self.color_primario}10"  # 10% de opacidad
#                 ctrl.border = ft.border.all(1, self.color_primario)
#                 ctrl.scale = ft.Scale(1.02)
                
#                 # Obtener el contenido del botón (diferente para botón con Stack)
#                 contenido = ctrl.content
                
#                 # Si es el botón de Alertas (con Stack)
#                 if index == 2 and isinstance(contenido, ft.Stack):
#                     # El contenido está en el primer elemento del Stack (índice 0)
#                     boton_container = contenido.controls[0]
#                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
#                         row_controls = boton_container.content.controls
#                         if len(row_controls) > 1:
#                             if hasattr(row_controls[0], 'color'):
#                                 row_controls[0].color = self.color_primario
#                             if hasattr(row_controls[1], 'color'):
#                                 row_controls[1].color = self.color_primario
#                 else:
#                     # Para botones normales
#                     if isinstance(contenido, ft.Row):
#                         row_controls = contenido.controls
#                         if len(row_controls) > 1:
#                             if hasattr(row_controls[0], 'color'):
#                                 row_controls[0].color = self.color_primario
#                             if hasattr(row_controls[1], 'color'):
#                                 row_controls[1].color = self.color_primario
#             else:
#                 ctrl.bgcolor = ft.Colors.WHITE
#                 ctrl.border = ft.border.all(1, self.color_borde)
#                 ctrl.scale = ft.Scale(1.0)
                
#                 # Obtener el contenido del botón
#                 contenido = ctrl.content
                
#                 # Si es el botón de Alertas (con Stack)
#                 if index == 2 and isinstance(contenido, ft.Stack):
#                     boton_container = contenido.controls[0]
#                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
#                         row_controls = boton_container.content.controls
#                         if len(row_controls) > 1:
#                             if hasattr(row_controls[0], 'color'):
#                                 row_controls[0].color = self.color_texto_secundario
#                             if hasattr(row_controls[1], 'color'):
#                                 row_controls[1].color = self.color_texto
#                 else:
#                     # Para botones normales
#                     if isinstance(contenido, ft.Row):
#                         row_controls = contenido.controls
#                         if len(row_controls) > 1:
#                             if hasattr(row_controls[0], 'color'):
#                                 row_controls[0].color = self.color_texto_secundario
#                             if hasattr(row_controls[1], 'color'):
#                                 row_controls[1].color = self.color_texto
        
#         # Usar try-except para evitar errores si la página no está lista
#         try:
#             ctrl.update()
#         except:
#             pass



#     def inicializar_alertas_view(self):
#         """Inicializa AlertasView después de que todo esté listo"""
#         self.alertas_view = AlertasView(self.sistema_alertas, self.page)
#         self.actualizar_alertas_container()
        
#         # Inicializar el contador de alertas DESPUÉS de que la página esté lista
#         self.page.run_thread(self.inicializar_contador_alertas)

#     def inicializar_contador_alertas(self):
#         """Inicializa el contador de alertas después de que la página esté lista"""
#         time.sleep(0.5)  # Pequeña espera para asegurar que la página esté lista
#         self.actualizar_contador_alertas()

#     def actualizar_alertas_container(self):
#         """Actualiza el contenedor de ALERTAS con el AlertasView"""
#         if self.alertas_view is None:
#             return
            
#         # ¡ASIGNAR AlertasView al calendar_container_1 (índice 2)!
#         self.calendar_container_1.content = ft.Column(
#             expand=True,
#             controls=[
#                 ft.Container(
#                     padding=10,
#                     bgcolor=ft.Colors.WHITE,
#                     border_radius=10,
#                     shadow=ft.BoxShadow(
#                         spread_radius=1,
#                         blur_radius=5,
#                         color=ft.Colors.GREY_300,
#                     ),
#                     content=ft.Row(
#                         alignment=ft.MainAxisAlignment.CENTER,
#                         controls=[
#                             ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, color=ft.Colors.RED_700, size=28),
#                             ft.Text(
#                                 "Historial de Alertas del Sistema",
#                                 size=20,
#                                 weight=ft.FontWeight.BOLD,
#                                 color=ft.Colors.BLUE_900
#                             ),
#                         ],
#                         spacing=15
#                     )
#                 ),
#                 ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
#                 ft.Container(
#                     expand=True,
#                     bgcolor=ft.Colors.WHITE,
#                     border_radius=15,
#                     padding=10,
#                     shadow=ft.BoxShadow(
#                         spread_radius=1,
#                         blur_radius=5,
#                         color=ft.Colors.GREY_300,
#                     ),
#                     content=self.alertas_view
#                 )
#             ]
#         )

#     def actualizar_contador_alertas(self):
#         """Actualiza el contador de alertas en el badge"""
#         if self.notificacion_badge is not None:
#             total_alertas = self.sistema_alertas.contar_alertas()
            
#             # NO mostrar el badge si estamos en la página de Alertas
#             if total_alertas > 0 and not self.en_pagina_alertas:
#                 self.notificacion_badge.visible = True
#                 self.notificacion_badge.content.value = str(total_alertas) if total_alertas <= 99 else "99+"
                
#                 # Si hay muchas alertas, hacer el badge más pequeño
#                 if total_alertas > 9:
#                     self.notificacion_badge.width = 24
#                     self.notificacion_badge.height = 20
#                 else:
#                     self.notificacion_badge.width = 20
#                     self.notificacion_badge.height = 20
#             else:
#                 self.notificacion_badge.visible = False
            
#             # Actualizar el badge de forma segura
#             try:
#                 self.notificacion_badge.update()
#             except Exception as e:
#                 print(f"Error actualizando badge: {e}")

#     def agregar_alerta_y_actualizar(self, causa, pagina):
#         """Agrega una alerta y actualiza la vista y el contador"""
#         # Agregar la alerta al sistema
#         self.sistema_alertas.agregar_alerta(causa, pagina)
        
#         # Actualizar el contador de notificaciones (solo si NO estamos en la página de Alertas)
#         self.actualizar_contador_alertas()
        
#         # Notificar a AlertasView si está en la página actual
#         if self.alertas_view is not None and hasattr(self.alertas_view, 'en_pagina') and self.alertas_view.en_pagina:
#             # Forzar actualización inmediata
#             self.page.run_thread(self.alertas_view.cargar_ui)
#             print(f"✓ Alerta agregada y vista actualizada: {causa}")

#     def registrar_manual(self, e=None):
#         """Registra un dato manualmente desde el botón en Home"""
#         print("Registro manual solicitado")
#         datos_actuales = self.obtener_datos_actuales_redondeados()
        
#         registro = self.reloj_global.agregar_al_historial(
#             datos_actuales, 
#             tipo="registro_manual", 
#             fuente="Manual (Home)"
#         )
        
#         # Usar el nuevo método
#         self.agregar_alerta_y_actualizar(
#             causa="Registro manual ejecutado desde Home",
#             pagina="UMA"
#         )
        
#         self.mostrar_notificacion("✓ Registro manual agregado", ft.Colors.GREEN)
    
#     def limpiar_historial_completamente(self, e=None):
#         """Limpia todo el historial"""
#         def confirmar_limpieza(e):
#             self.reloj_global.limpiar_historial()
#             dlg_modal.open = False
#             self.page.update()
#             self.mostrar_notificacion("✓ Historial limpiado", ft.Colors.GREEN)
            
#             # Usar el nuevo método
#             self.agregar_alerta_y_actualizar(
#                 causa="Historial de registros limpiado",
#                 pagina="UMA"
#             )
        
#         def cancelar_limpieza(e):
#             dlg_modal.open = False
#             self.page.update()
        
#         dlg_modal = ft.AlertDialog(
#             modal=True,
#             title=ft.Text("Confirmar limpieza"),
#             content=ft.Text("¿Está seguro que desea eliminar TODOS los registros del historial?\nEsta acción no se puede deshacer."),
#             actions=[
#                 ft.TextButton("Cancelar", on_click=cancelar_limpieza),
#                 ft.ElevatedButton(
#                     "Limpiar Todo", 
#                     on_click=confirmar_limpieza,
#                     bgcolor=ft.Colors.RED,
#                     color=ft.Colors.WHITE
#                 ),
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#         )
        
#         self.page.dialog = dlg_modal
#         dlg_modal.open = True
#         self.page.update()
    
#     def mostrar_notificacion(self, mensaje, color):
#         """Muestra una notificación temporal"""
#         snackbar = ft.SnackBar(
#             content=ft.Text(mensaje, color=ft.Colors.WHITE),
#             bgcolor=color,
#             duration=2000,
#         )
#         self.page.snack_bar = snackbar
#         snackbar.open = True
#         self.page.update()

#     def mostrar_banner_inicio(self):
#         self.banner.open = True
#         self.page.update()

#     def cerrar_banner(self, e):
#         self.banner.open = False
#         self.page.update()

#     def _on_alarma(self, hora):
#         """Se ejecuta cuando el reloj global detecta una alarma"""
#         print(f"UI: Alarma recibida: {hora}")
        
#         datos_actuales = self.obtener_datos_actuales_redondeados()
        
#         if hasattr(self, 'excel_manager'):
#             self.excel_manager.guardar_todos(datos_actuales)
            
#         registro = self.reloj_global.agregar_al_historial(
#             datos_actuales, 
#             tipo="registro_automatico", 
#             fuente=f"Alarma {hora}"
#         )
        
#         # Usar el nuevo método
#         self.agregar_alerta_y_actualizar(
#             causa=f"Registro automático ejecutado a las {hora}",
#             pagina="Reloj Global"
#         )
        
#         # FORZAR ACTUALIZACIÓN DE UMA INMEDIATAMENTE
#         if hasattr(self, 'uma_instance'):
#             self.page.run_thread(lambda: self.uma_instance.actualizar_lista())
        
#         self.mostrar_notificacion(f"✓ Registro automático a las {hora}", ft.Colors.BLUE)

#     def obtener_datos_actuales_redondeados(self):
#         """Obtiene los datos actuales redondeados"""
#         datos = self.datos_tiempo_real.copy()
#         datos['temperatura'] = round(datos['temperatura'], 1)
#         datos['humedad'] = round(datos['humedad'])
#         datos['presion1'] = round(datos['presion1'], 1)
#         datos['presion2'] = round(datos['presion2'], 1)
#         datos['presion3'] = round(datos['presion3'], 1)
#         return datos

#     def _initialize_ui_components(self):
#         """Inicializa todos los componentes de la interfaz de usuario"""

#         # 1. Crear controles de texto para UMA
#         self.txt_temp_home = ft.Text("-- °C", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
#         self.txt_hum_home = ft.Text("-- %", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
#         self.txt_pres_home = ft.Text("-- Pa", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
        
#         # 2. Crear UMA
#         self.uma_instance = UMA(
#             txt_temp=self.txt_temp_home,
#             txt_hum=self.txt_hum_home,
#             txt_pres=self.txt_pres_home,
#             page=self.page,
#             reloj_global=self.reloj_global
#         )

#         # 3. Crear manómetros
#         self.blue_box_presion1 = BlueBox(texto_titulo="MANOMETRO 1",texto=f"{self.datos_tiempo_real['presion1']} Pa", mostrar_boton=False)
#         self.blue_box_presion2 = BlueBox(texto_titulo="MANOMETRO 2",texto=f"{self.datos_tiempo_real['presion2']} Pa", mostrar_boton=False)
#         self.blue_box_presion3 = BlueBox(texto_titulo="MANOMETRO 3",texto=f"{self.datos_tiempo_real['presion3']} Pa", mostrar_boton=False)
        
#         self.blue_boxes = {
#             'presion1': self.blue_box_presion1,
#             'presion2': self.blue_box_presion2,
#             'presion3': self.blue_box_presion3,
#         }

#         self.config_container = ConfiguracionContainer(self.page, self.reloj_global)

#         # 4. Crear manómetros CON CALLBACKS
#         self.blue_box_presion1 = BlueBox(
#             texto_titulo="MANOMETRO 1",
#             texto=f"{self.datos_tiempo_real['presion1']} Pa", 
#             mostrar_boton=False,
#             # NUEVO: Callback para abrir página de gráfica
#             on_grafica_click=self.abrir_pagina_grafica
#         )
        
#         self.blue_box_presion2 = BlueBox(
#             texto_titulo="MANOMETRO 2",
#             texto=f"{self.datos_tiempo_real['presion2']} Pa", 
#             mostrar_boton=False,
#             on_grafica_click=self.abrir_pagina_grafica
#         )
        
#         self.blue_box_presion3 = BlueBox(
#             texto_titulo="MANOMETRO 3",
#             texto=f"{self.datos_tiempo_real['presion3']} Pa", 
#             mostrar_boton=False,
#             on_grafica_click=self.abrir_pagina_grafica
#         )
        
#         self.blue_boxes = {
#             'presion1': self.blue_box_presion1,
#             'presion2': self.blue_box_presion2,
#             'presion3': self.blue_box_presion3,
#         }

#         ################################### PAGINA 1 (UMA) ####################################
#         self.home_container_1 = ft.Container(
#             bgcolor=self.color_teal,
#             border_radius=20,
#             expand=True,
#             padding=20,
#             alignment=ft.alignment.center,
#             content=ft.Column(
#                 expand=True,
#                 controls=[
#                     self.uma_instance,
#                 ]
#             )
#         )

#         ################################### PAGINA 2 (MANOMETROS) ####################################
#         self.location_container_1 = ft.Container(
#             bgcolor=self.color_teal,
#             border_radius=20,
#             expand=True,
#             padding=20,
#             content=ft.Column(
#                 alignment=ft.MainAxisAlignment.START,
#                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                 expand=True,
#                 controls=[
#                     ft.Container(
#                         expand=True,
#                         bgcolor=ft.Colors.WHITE,
#                         border_radius=20,
#                         alignment=ft.alignment.center,
#                         padding=20,
#                         shadow=ft.BoxShadow(
#                             spread_radius=1,
#                             blur_radius=10,
#                             color=ft.Colors.GREY_300,
#                         ),
#                         content=ft.Column(
#                             scroll=ft.ScrollMode.AUTO,
#                             spacing=30,
#                             controls=[
#                                 ft.Row(
#                                     alignment=ft.MainAxisAlignment.CENTER,
#                                     vertical_alignment=ft.CrossAxisAlignment.CENTER,
#                                     spacing=30,
#                                     controls=[
#                                         self.blue_box_presion1,
#                                         self.blue_box_presion2,
#                                         self.blue_box_presion3,
#                                     ]
#                                 )
#                             ]
#                         )
#                     )
#                 ]
#             )
#         )

#         ################################### PAGINA 3 (ALERTAS) ####################################
#         # ¡ESTE ES EL CONTENEDOR DE ALERTAS!
#         self.calendar_container_1 = ft.Container(
#             bgcolor=self.color_teal,
#             border_radius=20,
#             expand=True,
#             padding=20,
#             content=ft.Container()  # Vacío por ahora, se llenará con AlertasView
#         )

#         ################################### PAGINA 4 (CONFIGURACION) ####################################
#         # ¡ESTE ES EL CONTENEDOR DE CONFIGURACIÓN (CON EL RELOJ)!
#         self.setting_container_1 = ft.Container(
#             bgcolor=self.color_teal,
#             border_radius=20,
#             expand=True,
#             padding=20,
#             content=ft.Column(
#                 alignment=ft.MainAxisAlignment.CENTER,
#                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                 expand=True,
#                 controls=[self.config_container]  # ConfiguraciónContainer va aquí (contiene el reloj)
#             )
#         )

#         ################################### PÁGINA 5 (GRÁFICAS) ####################################
#         # Los textos que se actualizarán dinámicamente
#         self.titulo_grafica_text = ft.Text(
#             value="Gráfica del Manómetro",
#             size=24,
#             weight=ft.FontWeight.BOLD,
#             color=ft.Colors.BLUE_900
#         )
        
#         # ¡IMPORTANTE! Este Text mostrará el valor ACTUAL en tiempo real
#         self.presion_actual_display = ft.Text(
#             value="-- Pa",  # Valor inicial
#             size=20,
#             weight=ft.FontWeight.BOLD,
#             color=ft.Colors.GREEN_700
#         )
        
#         self.grafica_container = ft.Container(
#             bgcolor=self.color_teal,
#             border_radius=20,
#             expand=True,
#             padding=20,
#             content=ft.Column(
#                 expand=True,
#                 spacing=20,
#                 controls=[
#                     # CABECERA
#                     ft.Container(
#                         padding=ft.padding.symmetric(vertical=10, horizontal=15),
#                         bgcolor=ft.Colors.WHITE,
#                         border_radius=10,
#                         shadow=ft.BoxShadow(
#                             spread_radius=1,
#                             blur_radius=5,
#                             color=ft.Colors.GREY_300,
#                         ),
#                         content=ft.Row(
#                             alignment=ft.MainAxisAlignment.START,
#                             vertical_alignment=ft.CrossAxisAlignment.CENTER,
#                             spacing=20,
#                             controls=[
#                                 ft.IconButton(
#                                     icon=ft.Icons.ARROW_BACK,
#                                     icon_color=ft.Colors.BLUE_700,
#                                     icon_size=28,
#                                     on_click=lambda e: self.change_page_manual(1),
#                                     tooltip="Volver a Manómetros"
#                                 ),
#                                 self.titulo_grafica_text
#                             ]
#                         )
#                     ),
                    
#                     # CONTENIDO PRINCIPAL
#                     ft.Container(
#                         expand=True,
#                         bgcolor=ft.Colors.WHITE,
#                         border_radius=15,
#                         padding=25,
#                         shadow=ft.BoxShadow(
#                             spread_radius=1,
#                             blur_radius=10,
#                             color=ft.Colors.GREY_300,
#                         ),
#                         content=ft.Column(
#                             expand=True,
#                             spacing=25,
#                             controls=[
#                                 # Información adicional
#                                 ft.Container(
#                                     padding=15,
#                                     bgcolor=ft.Colors.BLUE_50,
#                                     border_radius=10,
#                                     content=ft.Row(
#                                         spacing=10,
#                                         controls=[
#                                             ft.Text("Presión actual:", size=16, color=ft.Colors.GREY_600),
#                                             self.presion_actual_display,
#                                         ]
#                                     )
#                                 ),
#                                 ft.Row(
#                                     expand=True,
#                                     controls=[
#                                         # Panel izquierdo - Grafica
#                                         ft.Container(
#                                             # width=400,
#                                             # height=250,
#                                             expand=True,
#                                             padding=20,
#                                             bgcolor=ft.Colors.WHITE,
#                                             border_radius=10,
#                                             content=ft.Column(
#                                                 expand=True,
#                                                 spacing=10,
#                                                 controls=[
#                                                     ft.Row(
#                                                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                                                         controls=[
#                                                             ft.Text("Grafica", 
#                                                                 size=18, weight=ft.FontWeight.BOLD),
#                                                         ]
#                                                     ),
                                                    
#                                                     ft.Divider(height=1, color=ft.Colors.GREY_300),
                                                    
#                                                     # Área de historial
#                                                     ft.Container(
#                                                         expand=True,
#                                                         border=ft.border.all(1, ft.Colors.GREY_300),
#                                                         border_radius=10,
#                                                         padding=10,
#                                                         # content=self.lista_historial
#                                                     )
#                                                 ]
#                                             )
#                                         ),
#                                         # Panel derecho - Historial
#                                         ft.Container(
#                                             # width=400,
#                                             # height=250,
#                                             expand=True,
#                                             padding=20,
#                                             bgcolor=ft.Colors.WHITE,
#                                             border_radius=10,
#                                             content=ft.Column(
#                                                 expand=True,
#                                                 spacing=10,
#                                                 controls=[
#                                                     # ENCABEZADO DE TABLA ÚNICO (fuera de la lista)
#                                                     ft.Container(
#                                                         padding=10,
#                                                         bgcolor=ft.Colors.BLUE_100,
#                                                         border_radius=5,
#                                                         margin=ft.margin.only(bottom=5),
#                                                         content=ft.Row([
#                                                             # Causa (40% del ancho)
#                                                             ft.Container(
#                                                                 width=100,
#                                                                 content=ft.Text("Presion", 
#                                                                             weight=ft.FontWeight.BOLD,
#                                                                             color=ft.Colors.BLUE_800,
#                                                                             size=12)
#                                                             ),
#                                                             # Fuente (20%)
#                                                             ft.Container(
#                                                                 width=100,
#                                                                 content=ft.Text("Fecha", 
#                                                                             weight=ft.FontWeight.BOLD,
#                                                                             color=ft.Colors.BLUE_800,
#                                                                             size=12)
#                                                             ),
#                                                             # Fecha (15%)
#                                                             ft.Container(
#                                                                 width=100,
#                                                                 content=ft.Text("Hora", 
#                                                                             weight=ft.FontWeight.BOLD,
#                                                                             color=ft.Colors.BLUE_800,
#                                                                             size=12)
#                                                             ),
#                                                             # Hora (15%)
#                                                             ft.Container(
#                                                                 width=100,
#                                                                 content=ft.Text("Tipo", 
#                                                                             weight=ft.FontWeight.BOLD,
#                                                                             color=ft.Colors.BLUE_800,
#                                                                             size=12)
#                                                             ),
#                                                         ])
#                                                     ),
                                                    
#                                                     ft.Divider(height=1, color=ft.Colors.GREY_300),
                                                    
#                                                     # Área de historial
#                                                     ft.Container(
#                                                         expand=True,
#                                                         border=ft.border.all(1, ft.Colors.GREY_300),
#                                                         border_radius=10,
#                                                         padding=10,
#                                                         # content=self.lista_historial
#                                                     ),
                                                    
#                                                     # Leyenda
#                                                     ft.Container(
#                                                         padding=10,
#                                                         content=ft.Row(
#                                                             spacing=15,
#                                                             alignment=ft.MainAxisAlignment.CENTER,
#                                                             controls=[
#                                                                 ft.Row([
#                                                                     ft.Container(width=12, height=12, 
#                                                                             bgcolor=ft.Colors.BLUE_50, 
#                                                                             border_radius=6),
#                                                                     ft.Text("Automático", size=10),
#                                                                 ]),
#                                                                 ft.Row([
#                                                                     ft.Container(width=12, height=12, 
#                                                                             bgcolor=ft.Colors.GREEN_50, 
#                                                                             border_radius=6),
#                                                                     ft.Text("Manual", size=10),
#                                                                 ]),
#                                                             ]
#                                                         )
#                                                     )
#                                                 ]
#                                             )
#                                         )
#                                     ]
#                                 ),
#                                 # # Panel derecho - Historial
#                                 # ft.Container(
#                                 #     width=400,
#                                 #     height=250,
#                                 #     expand=True,
#                                 #     padding=20,
#                                 #     bgcolor=ft.Colors.WHITE,
#                                 #     border_radius=10,
#                                 #     content=ft.Column(
#                                 #         expand=True,
#                                 #         spacing=10,
#                                 #         controls=[
#                                 #             ft.Row(
#                                 #                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                                 #                 controls=[
#                                 #                     ft.Text("Historial de Registros", 
#                                 #                         size=18, weight=ft.FontWeight.BOLD),
#                                 #                     # self.contador,
#                                 #                     ft.Row(
#                                 #                         spacing=10,
#                                 #                         # controls=[self.btn_registro, self.btn_limpiar]
#                                 #                     )
#                                 #                 ]
#                                 #             ),
                                            
#                                 #             ft.Divider(height=1, color=ft.Colors.GREY_300),
                                            
#                                 #             # Área de historial
#                                 #             ft.Container(
#                                 #                 expand=True,
#                                 #                 border=ft.border.all(1, ft.Colors.GREY_300),
#                                 #                 border_radius=10,
#                                 #                 padding=10,
#                                 #                 # content=self.lista_historial
#                                 #             ),
                                            
#                                 #             # Leyenda
#                                 #             ft.Container(
#                                 #                 padding=10,
#                                 #                 content=ft.Row(
#                                 #                     spacing=15,
#                                 #                     alignment=ft.MainAxisAlignment.CENTER,
#                                 #                     controls=[
#                                 #                         ft.Row([
#                                 #                             ft.Container(width=12, height=12, 
#                                 #                                     bgcolor=ft.Colors.BLUE_50, 
#                                 #                                     border_radius=6),
#                                 #                             ft.Text("Automático", size=10),
#                                 #                         ]),
#                                 #                         ft.Row([
#                                 #                             ft.Container(width=12, height=12, 
#                                 #                                     bgcolor=ft.Colors.GREEN_50, 
#                                 #                                     border_radius=6),
#                                 #                             ft.Text("Manual", size=10),
#                                 #                         ]),
#                                 #                     ]
#                                 #                 )
#                                 #             )
#                                 #         ]
#                                 #     )
#                                 # )
#                             ]
#                         )
#                     )
#                 ]
#             )
#         )

#         # NUEVO: Agregar la página de gráficas a la lista
#         self.container_list_1 = [
#             self.home_container_1,      # índice 0: UMA
#             self.location_container_1,  # índice 1: Manómetros  
#             self.calendar_container_1,  # índice 2: Alertas
#             self.setting_container_1,   # índice 3: Configuración
#             self.grafica_container      # NUEVO índice 4: Gráficas
#         ]

#         # self.container_list_1 = [
#         #     self.home_container_1,      # índice 0: UMA
#         #     self.location_container_1,  # índice 1: Manómetros  
#         #     self.calendar_container_1,  # índice 2: Alertas (vacío por ahora)
#         #     self.setting_container_1    # índice 3: Configuración (con el reloj)
#         # ]
        
#         self.container_1 = ft.Container(
#             content=self.container_list_1[0], 
#             expand=True,
#             animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
#         )

#         # ========== BARRA DE NAVEGACIÓN PROFESIONAL ==========
#         # Botones de navegación con diseño profesional
#         self.btn_connect = self._crear_boton_navegacion_profesional("UMA", ft.Icons.MONITOR_HEART, 0)
#         self.btn_connect2 = self._crear_boton_navegacion_profesional("Manómetros", ft.Icons.SPEED, 1)
#         self.btn_connect3 = self._crear_boton_navegacion_profesional("Alertas", ft.Icons.NOTIFICATIONS, 2)
#         self.btn_connect4 = self._crear_boton_navegacion_profesional("Configuración", ft.Icons.SETTINGS, 3)

#         # Barra lateral de navegación profesional
#         self.navigation_container = ft.Container(
#             col=2,
#             expand=True,
#             bgcolor=ft.Colors.WHITE,
#             border_radius=0,
#             border=ft.border.only(right=ft.border.BorderSide(1, self.color_borde)),
#             padding=ft.padding.symmetric(vertical=30, horizontal=20),
#             shadow=ft.BoxShadow(
#                 spread_radius=0,
#                 blur_radius=20,
#                 color="rgba(39, 245, 180, 0.08)",
#                 offset=ft.Offset(5, 0)
#             ),
#             content=ft.Column(
#                 alignment=ft.MainAxisAlignment.START,
#                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                 expand=True,
#                 spacing=15,
#                 controls=[
#                     # Logo y nombre
#                     ft.Container(
#                         padding=ft.padding.only(bottom=30),
#                         content=ft.Column(
#                             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                             spacing=10,
#                             controls=[
#                                 ft.Container(
#                                     width=60,
#                                     height=60,
#                                     border_radius=15,
#                                     bgcolor=self.color_primario,
#                                     alignment=ft.alignment.center,
#                                     shadow=ft.BoxShadow(
#                                         spread_radius=0,
#                                         blur_radius=15,
#                                         color="rgba(39, 245, 180, 0.15)",
#                                     ),
#                                     content=ft.Icon(
#                                         ft.Icons.MONITOR_HEART,
#                                         color=ft.Colors.WHITE,
#                                         size=30
#                                     )
#                                 ),
#                                 ft.Column(
#                                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                                     spacing=2,
#                                     controls=[
#                                         ft.Text(
#                                             "Sistema de",
#                                             size=14,
#                                             weight=ft.FontWeight.BOLD,
#                                             color=self.color_texto
#                                         ),
#                                         ft.Text(
#                                             "Monitoreo",
#                                             size=14,
#                                             weight=ft.FontWeight.BOLD,
#                                             color=self.color_primario
#                                         )
#                                     ]
#                                 )
#                             ]
#                         )
#                     ),
                    
#                     ft.Divider(height=20, color=self.color_borde),
                    
#                     # Botones de navegación
#                     self.btn_connect,
#                     self.btn_connect2,
#                     self.btn_connect3,
#                     self.btn_connect4,
                    
#                     ft.Divider(height=30, color=self.color_borde),
                    
#                     # Estado del sistema
#                     ft.Container(
#                         padding=15,
#                         bgcolor=f"{self.color_primario}08",
#                         border_radius=10,
#                         content=ft.Column(
#                             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                             spacing=8,
#                             controls=[
#                                 ft.Row(
#                                     spacing=8,
#                                     controls=[
#                                         ft.Container(
#                                             width=10,
#                                             height=10,
#                                             border_radius=5,
#                                             bgcolor=self.color_primario
#                                         ),
#                                         ft.Text(
#                                             "Sistema Activo",
#                                             size=12,
#                                             weight=ft.FontWeight.W_600,
#                                             color=self.color_texto
#                                         )
#                                     ]
#                                 ),
#                                 ft.Text(
#                                     datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
#                                     size=11,
#                                     color=self.color_texto_secundario
#                                 )
#                             ]
#                         )
#                     )
#                 ]
#             )
#         )

#         # Área principal de contenido
#         self.frame_2 = ft.Container(
#             col=10,
#             alignment=ft.alignment.center,
#             bgcolor=self.color_teal,
#             expand=True,
#             content=ft.Column(
#                 expand=True,
#                 controls=[
#                     self.container_1,
#                 ]
#             )   
#         )
        
#         # Layout principal
#         self.resp_container = ft.ResponsiveRow(
#             vertical_alignment=ft.CrossAxisAlignment.STRETCH,
#             controls=[
#                 self.navigation_container,
#                 self.frame_2,
#             ]
#         )

#         self.iniciar_home_random()
        
#         # Inicializar botón activo
#         self.actualizar_colores_botones(0)

#     def redondear_entero_desde_6(self, valor):
#         """Redondea hacia arriba desde 0.6"""
#         parte_entera = int(valor)
#         decimal = valor - parte_entera
#         return parte_entera + 1 if decimal >= 0.6 else parte_entera
    
#     def generar_datos_random(self):
#         """Genera datos aleatorios con verificación de alertas"""
#         temp_original = random.uniform(15, 35)
#         hum_original = random.uniform(30, 90)
#         pres1_original = random.uniform(80, 110)
#         pres2_original = random.uniform(80, 110)
#         pres3_original = random.uniform(80, 110)

#         temp = self.redondear_entero_desde_6(temp_original)
#         hum = self.redondear_entero_desde_6(hum_original)
#         pres1 = self.redondear_entero_desde_6(pres1_original)
#         pres2 = self.redondear_entero_desde_6(pres2_original)
#         pres3 = self.redondear_entero_desde_6(pres3_original)

#         self.datos_tiempo_real = {
#             'temperatura': temp,
#             'humedad': hum, 
#             'presion1': pres1,
#             'presion2': pres2,
#             'presion3': pres3,
#         }

#         # Actualizar manómetros
#         for key, box in self.blue_boxes.items():
#             if hasattr(box, 'actualizar_valor'):
#                 valor = self.datos_tiempo_real[key]
#                 box.actualizar_valor(f"{valor} Pa")

#         # Verificar alertas - usar el nuevo método
#         if temp > 30:
#             self.agregar_alerta_y_actualizar(
#                 causa=f"Temperatura CRÍTICA: {temp}°C (supera 30°C)",
#                 pagina="UMA"
#             )
        
#         if hum > 85:
#             self.agregar_alerta_y_actualizar(
#                 causa=f"Humedad ALTA: {hum}% (superior a 85%)",
#                 pagina="UMA"
#             )
        
#         if pres1 > 108:
#             self.agregar_alerta_y_actualizar(
#                 causa=f"Presión ALTA: {pres1}Pa (supera 108 Pa)",
#                 pagina="UMA"
#             )
        
#         if pres2 > 108:
#             self.agregar_alerta_y_actualizar(
#                 causa=f"Presión ALTA: {pres2}Pa (supera 108 Pa)",
#                 pagina="UMA"
#             )
        
#         if pres3 > 108:
#             self.agregar_alerta_y_actualizar(
#                 causa=f"Presión ALTA: {pres3}Pa (supera 108 Pa)",
#                 pagina="UMA"
#             )
        
#         return {"presion1": pres1, "presion2": pres2, "presion3": pres3, "temperatura": temp, "humedad": hum}
    
#     # def iniciar_home_random(self):
#     #     """Inicia la generación aleatoria de datos"""
#     #     def loop():
#     #         while True:
#     #             datos = self.generar_datos_random()
                
#     #             def actualizar():
#     #                 # Actualiza los controles que UMA usa
#     #                 self.txt_temp_home.value = f"{datos['temperatura']} °C"
#     #                 self.txt_hum_home.value = f"{datos['humedad']} %"
#     #                 self.txt_pres_home.value = f"{datos['presion1']} Pa"
#     #                 self.page.update()
                
#     #             self.page.run_thread(actualizar)
#     #             time.sleep(2)
        
#     #     threading.Thread(target=loop, daemon=True).start()

#     def iniciar_home_random(self):
#         """Inicia la generación aleatoria de datos"""
#         def loop():
#             while True:
#                 datos = self.generar_datos_random()
                
#                 def actualizar():
#                     # Actualiza los controles que UMA usa
#                     self.txt_temp_home.value = f"{datos['temperatura']} °C"
#                     self.txt_hum_home.value = f"{datos['humedad']} %"
#                     self.txt_pres_home.value = f"{datos['presion1']} Pa"
                    
#                     # ¡NUEVO! Actualizar también la página de gráficas si estamos en ella
#                     if (hasattr(self, 'manometro_activo') and 
#                         hasattr(self, 'presion_actual_display') and
#                         self.container_1.content == self.grafica_container):
                        
#                         # Obtener el valor directamente como dijiste
#                         if "MANOMETRO 1" in self.manometro_activo:
#                             self.presion_actual_display.value = f"{self.datos_tiempo_real['presion1']} Pa"
#                         elif "MANOMETRO 2" in self.manometro_activo:
#                             self.presion_actual_display.value = f"{self.datos_tiempo_real['presion2']} Pa"
#                         elif "MANOMETRO 3" in self.manometro_activo:
#                             self.presion_actual_display.value = f"{self.datos_tiempo_real['presion3']} Pa"
                    
#                     self.page.update()
                
#                 self.page.run_thread(actualizar)
#                 time.sleep(2)  # Ya tienes este intervalo
        
#         threading.Thread(target=loop, daemon=True).start()

#     def change_page_manual(self, index):
#         """Cambia entre páginas de la aplicación"""
#         self.container_1.content = self.container_list_1[index]
#         self.actualizar_colores_botones(index)
        
#         # Actualizar estado de la página de Alertas
#         if index == 2:  # Si estamos entrando a Alertas
#             self.en_pagina_alertas = True
#             # Ocultar el badge
#             if self.notificacion_badge is not None:
#                 self.notificacion_badge.visible = False
#                 try:
#                     self.notificacion_badge.update()
#                 except:
#                     pass
#         else:  # Si estamos saliendo de Alertas
#             self.en_pagina_alertas = False
#             # Actualizar el contador para que se muestre si hay alertas
#             self.actualizar_contador_alertas()
        
#         if self.alertas_view is not None:
#             if index == 2:  # Alertas está en índice 2
#                 if hasattr(self.alertas_view, 'entrar_a_pagina'):
#                     self.alertas_view.entrar_a_pagina()
#             else:
#                 if hasattr(self.alertas_view, 'salir_de_pagina'):
#                     self.alertas_view.salir_de_pagina()

#         self.page.update()
    
#     # def actualizar_colores_botones(self, index_activo):
#     #     """Actualiza los colores y formas de los botones de navegación"""
#     #     botones = [self.btn_connect, self.btn_connect2, self.btn_connect3, self.btn_connect4]
        
#     #     for i, btn in enumerate(botones):
#     #         if i == index_activo:
#     #             # Botón activo: Color primario con fondo
#     #             btn.bgcolor = self.color_primario
#     #             btn.border = ft.border.all(1, self.color_primario)
#     #             # Cambiar color del icono y texto a blanco
#     #             if len(btn.content.controls[0].controls) > 0:
#     #                 row_controls = btn.content.controls[0].controls
#     #                 if hasattr(row_controls[0], 'color'):
#     #                     row_controls[0].color = ft.Colors.WHITE
#     #                 if hasattr(row_controls[1], 'color'):
#     #                     row_controls[1].color = ft.Colors.WHITE
#     #             btn.scale = ft.Scale(1.0)
#     #         else:
#     #             # Botones inactivos: Blanco con borde gris
#     #             btn.bgcolor = ft.Colors.WHITE
#     #             btn.border = ft.border.all(1, self.color_borde)
#     #             # Cambiar color del icono y texto a gris
#     #             if len(btn.content.controls[0].controls) > 0:
#     #                 row_controls = btn.content.controls[0].controls
#     #                 if hasattr(row_controls[0], 'color'):
#     #                     row_controls[0].color = self.color_texto_secundario
#     #                 if hasattr(row_controls[1], 'color'):
#     #                     row_controls[1].color = self.color_texto
#     #             btn.scale = ft.Scale(1.0)
        
#     #     # Actualizar todos los botones de forma segura
#     #     for btn in botones:
#     #         try:
#     #             btn.update()
#     #         except:
#     #             pass

#     def actualizar_colores_botones(self, index_activo):
#         """Actualiza los colores y formas de los botones de navegación"""
#         botones = [self.btn_connect, self.btn_connect2, self.btn_connect3, self.btn_connect4]
        
#         for i, btn in enumerate(botones):
#             if i == index_activo:
#                 # Botón activo: Color primario con fondo
#                 btn.bgcolor = self.color_primario
#                 btn.border = ft.border.all(1, self.color_primario)
                
#                 # Obtener el contenido del botón
#                 contenido = btn.content
                
#                 # Si es el botón de Alertas (con Stack)
#                 if i == 2 and isinstance(contenido, ft.Stack):
#                     boton_container = contenido.controls[0]
#                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
#                         row_controls = boton_container.content.controls
#                         if len(row_controls) > 1:
#                             if hasattr(row_controls[0], 'color'):
#                                 row_controls[0].color = ft.Colors.WHITE
#                             if hasattr(row_controls[1], 'color'):
#                                 row_controls[1].color = ft.Colors.WHITE
#                 else:
#                     # Para botones normales
#                     if isinstance(contenido, ft.Row):
#                         row_controls = contenido.controls
#                         if len(row_controls) > 1:
#                             if hasattr(row_controls[0], 'color'):
#                                 row_controls[0].color = ft.Colors.WHITE
#                             if hasattr(row_controls[1], 'color'):
#                                 row_controls[1].color = ft.Colors.WHITE
#                 btn.scale = ft.Scale(1.0)
#             else:
#                 # Botones inactivos: Blanco con borde gris
#                 btn.bgcolor = ft.Colors.WHITE
#                 btn.border = ft.border.all(1, self.color_borde)
                
#                 # Obtener el contenido del botón
#                 contenido = btn.content
                
#                 # Si es el botón de Alertas (con Stack)
#                 if i == 2 and isinstance(contenido, ft.Stack):
#                     boton_container = contenido.controls[0]
#                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
#                         row_controls = boton_container.content.controls
#                         if len(row_controls) > 1:
#                             if hasattr(row_controls[0], 'color'):
#                                 row_controls[0].color = self.color_texto_secundario
#                             if hasattr(row_controls[1], 'color'):
#                                 row_controls[1].color = self.color_texto
#                 else:
#                     # Para botones normales
#                     if isinstance(contenido, ft.Row):
#                         row_controls = contenido.controls
#                         if len(row_controls) > 1:
#                             if hasattr(row_controls[0], 'color'):
#                                 row_controls[0].color = self.color_texto_secundario
#                             if hasattr(row_controls[1], 'color'):
#                                 row_controls[1].color = self.color_texto
#                 btn.scale = ft.Scale(1.0)
        
#         # Actualizar todos los botones de forma segura
#         for btn in botones:
#             try:
#                 btn.update()
#             except:
#                 pass

#     def will_unmount(self):
#         """Detener el reloj global al cerrar la app"""
#         self.reloj_global.detener()

#     def abrir_pagina_grafica(self, titulo_manometro):
#         """Abre la página de gráficas para un manómetro específico"""
#         print(f"Abriendo gráfica para: {titulo_manometro}")
        
#         # 1. Guardar referencia al manómetro activo
#         self.manometro_activo = titulo_manometro
        
#         # 2. Obtener datos del manómetro específico
#         if "MANOMETRO 1" in titulo_manometro:
#             datos = self.datos_tiempo_real['presion1']
#         elif "MANOMETRO 2" in titulo_manometro:
#             datos = self.datos_tiempo_real['presion2']
#         elif "MANOMETRO 3" in titulo_manometro:
#             datos = self.datos_tiempo_real['presion3']
#         else:
#             datos = 0
        
#         # 3. Actualizar el título de la página
#         self.titulo_grafica_text.value = f"Gráfica: {titulo_manometro}"
        
#         # 4. Actualizar el valor inicial en el display
#         self.presion_actual_display.value = f"{datos} Pa"
        
#         # 5. Cambiar a la página de gráficas (índice 4)
#         self.change_page_manual(4)
        
#         # 6. Imprimir confirmación
#         print(f"✓ Página de gráficas abierta para {titulo_manometro}")
#         print(f"  Presión actual: {datos} Pa")


# def main(page: ft.Page):
#     page.title = "Sistema de Monitoreo Inteligente"
#     page.window.width = 1400
#     page.window.height = 750
#     page.window.resizable = True
#     page.horizontal_alignment = "center"
#     page.vertical_alignment = "center"
#     page.theme_mode = ft.ThemeMode.LIGHT
#     page.window.bgcolor = ft.Colors.WHITE
#     page.padding = 0

#     ui = UI(page)
#     page.add(ui)

# if __name__ == "__main__":
#     ft.app(target=main)














# # import flet as ft
# # import threading
# # import time
# # import datetime
# # import json
# # import os
# # import random
# # from cajaAzul import BlueBox
# # from configuracion import ConfiguracionContainer
# # from excel5 import ExcelUnicoArchivo
# # from alertas import SistemaAlertas, AlertasView
# # from paguina1 import UMA

# # class RelojGlobal:
# #     def __init__(self):
# #         self.horas_registradas = []
# #         self.archivo_horas = "horas.json"
# #         self.historial_registros = []
# #         self.archivo_historial = "historial_registros.json"
# #         self.reloj_activo = True
# #         self.ultima_ejecucion = {}
# #         self.callbacks = []
# #         self.historial_callbacks = []
        
# #         # Cargar horas guardadas
# #         self.cargar_horas()
# #         self.cargar_historial()
# #         self.iniciar()

# #     def agregar_callback(self, callback):
# #         """Agrega una función que se ejecutará cuando suene una alarma"""
# #         self.callbacks.append(callback)
    
# #     def agregar_callback_historial(self, callback):
# #         """Agrega una función que se ejecutará cuando se agregue un nuevo registro al historial"""
# #         self.historial_callbacks.append(callback)

# #     def cargar_horas(self):
# #         """Carga las horas desde archivo JSON"""
# #         if os.path.exists(self.archivo_horas):
# #             try:
# #                 with open(self.archivo_horas, "r") as file:
# #                     datos = json.load(file)
# #                     self.horas_registradas = [
# #                         datetime.datetime.strptime(h, "%H:%M").time()
# #                         for h in datos
# #                     ]
# #                 print(f"RelojGlobal: Horas cargadas: {[h.strftime('%I:%M %p') for h in self.horas_registradas]}")
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error cargando horas: {e}")
# #                 self.horas_registradas = []
    
# #     def cargar_historial(self):
# #         """Carga el historial desde archivo JSON"""
# #         if os.path.exists(self.archivo_historial):
# #             try:
# #                 with open(self.archivo_historial, "r") as file:
# #                     self.historial_registros = json.load(file)
# #                 print(f"RelojGlobal: Historial cargado ({len(self.historial_registros)} registros)")
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error cargando historial: {e}")
# #                 self.historial_registros = []
# #         else:
# #             self.guardar_historial()

# #     def guardar_horas(self):
# #         """Guarda las horas en archivo JSON"""
# #         try:
# #             datos = [h.strftime("%H:%M") for h in self.horas_registradas]
# #             with open(self.archivo_horas, "w") as file:
# #                 json.dump(datos, file)
# #         except Exception as e:
# #             print(f"RelojGlobal: Error guardando horas: {e}")
    
# #     def guardar_historial(self):
# #         """Guarda el historial en archivo JSON"""
# #         try:
# #             if len(self.historial_registros) > 50:
# #                 self.historial_registros = self.historial_registros[-50:]
            
# #             with open(self.archivo_historial, "w") as file:
# #                 json.dump(self.historial_registros, file, indent=2)
# #         except Exception as e:
# #             print(f"RelojGlobal: Error guardando historial: {e}")

# #     def agregar_hora(self, hora_time):
# #         """Agrega una hora a la lista global"""
# #         if hora_time not in self.horas_registradas:
# #             self.horas_registradas.append(hora_time)
# #             self.guardar_horas()
# #             print(f"RelojGlobal: Hora agregada: {hora_time.strftime('%I:%M %p')}")
# #             return True
# #         return False

# #     def eliminar_hora(self, hora_time):
# #         """Elimina una hora de la lista global"""
# #         if hora_time in self.horas_registradas:
# #             self.horas_registradas.remove(hora_time)
# #             self.guardar_horas()
# #             print(f"RelojGlobal: Hora eliminada: {hora_time.strftime('%I:%M %p')}")
# #             return True
# #         return False
    
# #     def agregar_al_historial(self, datos, tipo="registro_automatico", fuente="Reloj Global"):
# #         """Agrega un registro al historial"""
# #         registro = {
# #             "fecha": datetime.datetime.now().strftime("%d/%m/%y"),
# #             "hora": datetime.datetime.now().strftime("%H:%M"),
# #             "datos": datos,
# #             "tipo": tipo,
# #             "fuente": fuente
# #         }
# #         self.historial_registros.append(registro)
# #         self.guardar_historial()
        
# #         # Notificar a todos los callbacks
# #         for callback in self.historial_callbacks:
# #             try:
# #                 callback()
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error en callback de historial: {e}")
        
# #         return registro
    
# #     def obtener_registros_por_manometro(self, manometro_numero):
# #         """
# #         Obtiene todos los registros históricos para un manómetro específico.
# #         manometro_numero: 1, 2 o 3
# #         """
# #         registros_manometro = []
        
# #         for registro in self.historial_registros:
# #             if 'datos' in registro:
# #                 datos = registro['datos']
# #                 # Extraer la presión del manómetro específico
# #                 clave_presion = f'presion{manometro_numero}'
# #                 if clave_presion in datos:
# #                     registro_manometro = {
# #                         'fecha': registro['fecha'],
# #                         'hora': registro['hora'],
# #                         'presion': datos[clave_presion],
# #                         'tipo': registro.get('tipo', 'desconocido'),
# #                         'fuente': registro.get('fuente', 'desconocido'),
# #                         'temperatura': datos.get('temperatura', 0),
# #                         'humedad': datos.get('humedad', 0)
# #                     }
# #                     registros_manometro.append(registro_manometro)
        
# #         # Ordenar por fecha y hora (más reciente primero)
# #         registros_manometro.sort(
# #             key=lambda x: datetime.datetime.strptime(f"{x['fecha']} {x['hora']}", "%d/%m/%y %H:%M"),
# #             reverse=True
# #         )
        
# #         return registros_manometro

# #     def limpiar_historial(self):
# #         """Limpia todo el historial"""
# #         self.historial_registros = []
# #         self.guardar_historial()
# #         print("RelojGlobal: Historial limpiado")
        
# #         # Notificar a los callbacks
# #         for callback in self.historial_callbacks:
# #             try:
# #                 callback()
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error en callback de limpieza: {e}")

# #     def iniciar(self):
# #         """Inicia el reloj global en un hilo separado"""
# #         if not hasattr(self, 'thread') or not self.thread.is_alive():
# #             self.thread = threading.Thread(target=self._loop, daemon=True)
# #             self.thread.start()
# #             print("RelojGlobal: Iniciado")

# #     def _loop(self):
# #         """Loop principal del reloj"""
# #         while self.reloj_activo:
# #             try:
# #                 ahora = datetime.datetime.now()
                
# #                 for hora_obj in self.horas_registradas:
# #                     hora_actual_minuto = ahora.strftime("%I:%M %p")
# #                     segundos = ahora.strftime("%S")
# #                     hora_objetivo_str = hora_obj.strftime("%I:%M %p")

# #                     if hora_actual_minuto == hora_objetivo_str and segundos == "00":
# #                         h_obj = datetime.datetime.combine(ahora.date(), hora_obj)
# #                         clave = h_obj.strftime("%Y-%m-%d %H:%M")

# #                         if clave not in self.ultima_ejecucion:
# #                             self.ultima_ejecucion[clave] = True
# #                             self._ejecutar_alarma(hora_objetivo_str)
# #                             print(f"RelojGlobal: ✓ Alarma: {hora_objetivo_str}")
                
# #                 hoy = datetime.datetime.now().date()
# #                 claves_a_eliminar = [k for k in self.ultima_ejecucion 
# #                                     if datetime.datetime.strptime(k.split(" ")[0], "%Y-%m-%d").date() < hoy]
# #                 for k in claves_a_eliminar:
# #                     del self.ultima_ejecucion[k]

# #                 time.sleep(1)
                
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error en loop: {e}")
# #                 time.sleep(1)

# #     def _ejecutar_alarma(self, hora):
# #         """Ejecuta todos los callbacks registrados"""
# #         for callback in self.callbacks:
# #             try:
# #                 callback(hora)
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error en callback: {e}")

# #     def detener(self):
# #         """Detiene el reloj global"""
# #         self.reloj_activo = False


# # class UI(ft.Container):
# #     def __init__(self, page):
# #         super().__init__(expand=True)
# #         self.page = page
        
# #         # COLORES PARA LA BARRA DE NAVEGACIÓN
# #         self.color_primario = "#27F5B4"  # Verde agua
# #         self.color_fondo = "#FFFFFF"  # Blanco
# #         self.color_texto = "#2C3E50"  # Azul oscuro
# #         self.color_texto_secundario = "#6C757D"  # Gris
# #         self.color_borde = "#E9ECEF"  # Gris claro para bordes
        
# #         # Datos en tiempo real (manteniendo los originales)
# #         self.datos_tiempo_real = {
# #             'temperatura': 0,
# #             'humedad': 0, 
# #             'presion1': 0,
# #             'presion2': 0,
# #             'presion3': 0,
# #         }

# #         self.excel_manager = ExcelUnicoArchivo()
# #         self.bandera_excel = self.excel_manager.get_bandera_archivo()
        
# #         self.reloj_global = RelojGlobal()
# #         self.sistema_alertas = SistemaAlertas()
# #         self.alertas_view = None
        
# #         # Variable para el badge de notificaciones
# #         self.notificacion_badge = None
# #         # Variable para saber si estamos en la página de Alertas
# #         self.en_pagina_alertas = False
        
# #         # NUEVO: Para manejar la página de gráficas
# #         self.manometro_activo = None
# #         self.manometro_numero = None  # 1, 2 o 3
# #         self.historial_lista = None

# #         self.banner = ft.Banner(
# #             bgcolor=ft.Colors.AMBER_100,
# #             leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
# #             content=ft.Text(
# #                 "Sistema de monitoreo iniciado",
# #                 color=ft.Colors.BLACK,
# #             ),
# #             actions=[
# #                 ft.TextButton("OK", on_click=self.cerrar_banner)
# #             ],
# #         )
# #         self.page.controls.append(self.banner)

# #         if not self.bandera_excel:
# #             print("⚠️ Main: No se encontró archivo Excel, mostrando banner...")
# #             self.mostrar_banner_inicio()
# #         else:
# #             self.reloj_global.agregar_callback(self._on_alarma)
# #             print("✅ Main: Archivo Excel encontrado")

# #         self.color_teal = ft.Colors.GREY_300

# #         self._initialize_ui_components()
# #         self.content = self.resp_container
        
# #         self.inicializar_alertas_view()

# #     def _crear_boton_navegacion_profesional(self, texto, icono, index):
# #         """Crea un botón de navegación con diseño profesional y badge de notificaciones"""
        
# #         # Contenedor para el contenido del botón (icono + texto)
# #         contenido_boton = ft.Row(
# #             alignment=ft.MainAxisAlignment.CENTER,
# #             vertical_alignment=ft.CrossAxisAlignment.CENTER,
# #             spacing=15,
# #             controls=[
# #                 ft.Icon(icono, color=self.color_texto_secundario, size=22),
# #                 ft.Text(
# #                     texto, 
# #                     color=self.color_texto,
# #                     weight=ft.FontWeight.W_600,
# #                     size=14
# #                 )
# #             ]
# #         )
        
# #         # Crear el botón principal
# #         boton_principal = ft.Container(
# #             width=160,
# #             height=60,
# #             bgcolor=ft.Colors.WHITE,
# #             border_radius=10,
# #             border=ft.border.all(1, self.color_borde),
# #             alignment=ft.alignment.center,
# #             clip_behavior=ft.ClipBehavior.HARD_EDGE,
# #             animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
# #             on_hover=lambda e: self._on_hover_boton_nav(e, index),
# #             on_click=lambda e: self.change_page_manual(index),
# #         )
        
# #         # Si es el botón de Alertas, agregar el badge
# #         if index == 2:
# #             # Crear el badge
# #             badge = ft.Container(
# #                 width=20,
# #                 height=20,
# #                 border_radius=10,
# #                 bgcolor=ft.Colors.RED_600,
# #                 alignment=ft.alignment.center,
# #                 visible=False,
# #                 content=ft.Text(
# #                     "0",
# #                     size=10,
# #                     color=ft.Colors.WHITE,
# #                     weight=ft.FontWeight.BOLD
# #                 )
# #             )
            
# #             # Guardar referencia al badge
# #             self.notificacion_badge = badge
            
# #             # Crear el Stack con el botón y el badge
# #             stack_content = ft.Stack(
# #                 controls=[
# #                     # El contenido del botón (centrado)
# #                     ft.Container(
# #                         content=contenido_boton,
# #                         alignment=ft.alignment.center,
# #                         width=160,
# #                         height=60,
# #                     ),
# #                     # El badge posicionado en la esquina superior derecha
# #                     badge
# #                 ],
# #                 width=170,
# #                 height=65,
# #             )
            
# #             # Configurar el badge para que esté en la esquina superior derecha
# #             badge.top = 0
# #             badge.right = 0
            
# #             boton_principal.content = stack_content
# #             return boton_principal
# #         else:
# #             # Para otros botones, contenido simple
# #             boton_principal.content = contenido_boton
# #             return boton_principal

# #     def _on_hover_boton_nav(self, e, index):
# #         """Maneja el hover de los botones de navegación"""
# #         ctrl = e.control
# #         is_hover = (e.data == "true" or e.data is True)
        
# #         # Determinar qué botón está activo
# #         botones = [self.btn_connect, self.btn_connect2, self.btn_connect3, self.btn_connect4]
# #         index_activo = self.container_list_1.index(self.container_1.content) if self.container_1.content in self.container_list_1 else 0
        
# #         # Si no es el botón activo
# #         if index != index_activo:
# #             if is_hover:
# #                 ctrl.bgcolor = f"{self.color_primario}10"  # 10% de opacidad
# #                 ctrl.border = ft.border.all(1, self.color_primario)
# #                 ctrl.scale = ft.Scale(1.02)
                
# #                 # Obtener el contenido del botón (diferente para botón con Stack)
# #                 contenido = ctrl.content
                
# #                 # Si es el botón de Alertas (con Stack)
# #                 if index == 2 and isinstance(contenido, ft.Stack):
# #                     # El contenido está en el primer elemento del Stack (índice 0)
# #                     boton_container = contenido.controls[0]
# #                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
# #                         row_controls = boton_container.content.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_primario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_primario
# #                 else:
# #                     # Para botones normales
# #                     if isinstance(contenido, ft.Row):
# #                         row_controls = contenido.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_primario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_primario
# #             else:
# #                 ctrl.bgcolor = ft.Colors.WHITE
# #                 ctrl.border = ft.border.all(1, self.color_borde)
# #                 ctrl.scale = ft.Scale(1.0)
                
# #                 # Obtener el contenido del botón
# #                 contenido = ctrl.content
                
# #                 # Si es el botón de Alertas (con Stack)
# #                 if index == 2 and isinstance(contenido, ft.Stack):
# #                     boton_container = contenido.controls[0]
# #                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
# #                         row_controls = boton_container.content.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_texto_secundario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_texto
# #                 else:
# #                     # Para botones normales
# #                     if isinstance(contenido, ft.Row):
# #                         row_controls = contenido.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_texto_secundario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_texto
        
# #         # Usar try-except para evitar errores si la página no está lista
# #         try:
# #             ctrl.update()
# #         except:
# #             pass

# #     def inicializar_alertas_view(self):
# #         """Inicializa AlertasView después de que todo esté listo"""
# #         self.alertas_view = AlertasView(self.sistema_alertas, self.page)
# #         self.actualizar_alertas_container()
        
# #         # Inicializar el contador de alertas DESPUÉS de que la página esté lista
# #         self.page.run_thread(self.inicializar_contador_alertas)

# #     def inicializar_contador_alertas(self):
# #         """Inicializa el contador de alertas después de que la página esté lista"""
# #         time.sleep(0.5)
# #         self.actualizar_contador_alertas()

# #     def actualizar_alertas_container(self):
# #         """Actualiza el contenedor de ALERTAS con el AlertasView"""
# #         if self.alertas_view is None:
# #             return
            
# #         self.calendar_container_1.content = ft.Column(
# #             expand=True,
# #             controls=[
# #                 ft.Container(
# #                     padding=10,
# #                     bgcolor=ft.Colors.WHITE,
# #                     border_radius=10,
# #                     shadow=ft.BoxShadow(
# #                         spread_radius=1,
# #                         blur_radius=5,
# #                         color=ft.Colors.GREY_300,
# #                     ),
# #                     content=ft.Row(
# #                         alignment=ft.MainAxisAlignment.CENTER,
# #                         controls=[
# #                             ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, color=ft.Colors.RED_700, size=28),
# #                             ft.Text(
# #                                 "Historial de Alertas del Sistema",
# #                                 size=20,
# #                                 weight=ft.FontWeight.BOLD,
# #                                 color=ft.Colors.BLUE_900
# #                             ),
# #                         ],
# #                         spacing=15
# #                     )
# #                 ),
# #                 ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
# #                 ft.Container(
# #                     expand=True,
# #                     bgcolor=ft.Colors.WHITE,
# #                     border_radius=15,
# #                     padding=10,
# #                     shadow=ft.BoxShadow(
# #                         spread_radius=1,
# #                         blur_radius=5,
# #                         color=ft.Colors.GREY_300,
# #                     ),
# #                     content=self.alertas_view
# #                 )
# #             ]
# #         )

# #     def actualizar_contador_alertas(self):
# #         """Actualiza el contador de alertas en el badge"""
# #         if self.notificacion_badge is not None:
# #             total_alertas = self.sistema_alertas.contar_alertas()
            
# #             # NO mostrar el badge si estamos en la página de Alertas
# #             if total_alertas > 0 and not self.en_pagina_alertas:
# #                 self.notificacion_badge.visible = True
# #                 self.notificacion_badge.content.value = str(total_alertas) if total_alertas <= 99 else "99+"
                
# #                 # Si hay muchas alertas, hacer el badge más pequeño
# #                 if total_alertas > 9:
# #                     self.notificacion_badge.width = 24
# #                     self.notificacion_badge.height = 20
# #                 else:
# #                     self.notificacion_badge.width = 20
# #                     self.notificacion_badge.height = 20
# #             else:
# #                 self.notificacion_badge.visible = False
            
# #             # Actualizar el badge de forma segura
# #             try:
# #                 self.notificacion_badge.update()
# #             except Exception as e:
# #                 print(f"Error actualizando badge: {e}")

# #     def agregar_alerta_y_actualizar(self, causa, pagina):
# #         """Agrega una alerta y actualiza la vista y el contador"""
# #         # Agregar la alerta al sistema
# #         self.sistema_alertas.agregar_alerta(causa, pagina)
        
# #         # Actualizar el contador de notificaciones
# #         self.actualizar_contador_alertas()
        
# #         # Notificar a AlertasView si está en la página actual
# #         if self.alertas_view is not None and hasattr(self.alertas_view, 'en_pagina') and self.alertas_view.en_pagina:
# #             self.page.run_thread(self.alertas_view.cargar_ui)
# #             print(f"✓ Alerta agregada y vista actualizada: {causa}")

# #     def registrar_manual(self, e=None):
# #         """Registra un dato manualmente desde el botón en Home"""
# #         print("Registro manual solicitado")
# #         datos_actuales = self.obtener_datos_actuales_redondeados()
        
# #         registro = self.reloj_global.agregar_al_historial(
# #             datos_actuales, 
# #             tipo="registro_manual", 
# #             fuente="Manual (Home)"
# #         )
        
# #         self.agregar_alerta_y_actualizar(
# #             causa="Registro manual ejecutado desde Home",
# #             pagina="UMA"
# #         )
        
# #         self.mostrar_notificacion("✓ Registro manual agregado", ft.Colors.GREEN)
    
# #     def limpiar_historial_completamente(self, e=None):
# #         """Limpia todo el historial"""
# #         def confirmar_limpieza(e):
# #             self.reloj_global.limpiar_historial()
# #             dlg_modal.open = False
# #             self.page.update()
# #             self.mostrar_notificacion("✓ Historial limpiado", ft.Colors.GREEN)
            
# #             self.agregar_alerta_y_actualizar(
# #                 causa="Historial de registros limpiado",
# #                 pagina="UMA"
# #             )
        
# #         def cancelar_limpieza(e):
# #             dlg_modal.open = False
# #             self.page.update()
        
# #         dlg_modal = ft.AlertDialog(
# #             modal=True,
# #             title=ft.Text("Confirmar limpieza"),
# #             content=ft.Text("¿Está seguro que desea eliminar TODOS los registros del historial?\nEsta acción no se puede deshacer."),
# #             actions=[
# #                 ft.TextButton("Cancelar", on_click=cancelar_limpieza),
# #                 ft.ElevatedButton(
# #                     "Limpiar Todo", 
# #                     on_click=confirmar_limpieza,
# #                     bgcolor=ft.Colors.RED,
# #                     color=ft.Colors.WHITE
# #                 ),
# #             ],
# #             actions_alignment=ft.MainAxisAlignment.END,
# #         )
        
# #         self.page.dialog = dlg_modal
# #         dlg_modal.open = True
# #         self.page.update()
    
# #     def mostrar_notificacion(self, mensaje, color):
# #         """Muestra una notificación temporal"""
# #         snackbar = ft.SnackBar(
# #             content=ft.Text(mensaje, color=ft.Colors.WHITE),
# #             bgcolor=color,
# #             duration=2000,
# #         )
# #         self.page.snack_bar = snackbar
# #         snackbar.open = True
# #         self.page.update()

# #     def mostrar_banner_inicio(self):
# #         self.banner.open = True
# #         self.page.update()

# #     def cerrar_banner(self, e):
# #         self.banner.open = False
# #         self.page.update()

# #     def _on_alarma(self, hora):
# #         """Se ejecuta cuando el reloj global detecta una alarma"""
# #         print(f"UI: Alarma recibida: {hora}")
        
# #         datos_actuales = self.obtener_datos_actuales_redondeados()
        
# #         if hasattr(self, 'excel_manager'):
# #             self.excel_manager.guardar_todos(datos_actuales)
            
# #         registro = self.reloj_global.agregar_al_historial(
# #             datos_actuales, 
# #             tipo="registro_automatico", 
# #             fuente=f"Alarma {hora}"
# #         )
        
# #         self.agregar_alerta_y_actualizar(
# #             causa=f"Registro automático ejecutado a las {hora}",
# #             pagina="Reloj Global"
# #         )
        
# #         # FORZAR ACTUALIZACIÓN DE UMA INMEDIATAMENTE
# #         if hasattr(self, 'uma_instance'):
# #             self.page.run_thread(lambda: self.uma_instance.actualizar_lista())
        
# #         # Si estamos en la página de gráficas, actualizar el historial
# #         if (self.container_1.content == self.grafica_container and 
# #             self.manometro_numero is not None):
# #             self.actualizar_historial_manometro()
        
# #         self.mostrar_notificacion(f"✓ Registro automático a las {hora}", ft.Colors.BLUE)

# #     def obtener_datos_actuales_redondeados(self):
# #         """Obtiene los datos actuales redondeados"""
# #         datos = self.datos_tiempo_real.copy()
# #         datos['temperatura'] = round(datos['temperatura'], 1)
# #         datos['humedad'] = round(datos['humedad'])
# #         datos['presion1'] = round(datos['presion1'], 1)
# #         datos['presion2'] = round(datos['presion2'], 1)
# #         datos['presion3'] = round(datos['presion3'], 1)
# #         return datos

# #     def _initialize_ui_components(self):
# #         """Inicializa todos los componentes de la interfaz de usuario"""
        
# #         # 1. Crear controles de texto para UMA
# #         self.txt_temp_home = ft.Text("-- °C", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
# #         self.txt_hum_home = ft.Text("-- %", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
# #         self.txt_pres_home = ft.Text("-- Pa", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
        
# #         # 2. Crear UMA
# #         self.uma_instance = UMA(
# #             txt_temp=self.txt_temp_home,
# #             txt_hum=self.txt_hum_home,
# #             txt_pres=self.txt_pres_home,
# #             page=self.page,
# #             reloj_global=self.reloj_global
# #         )

# #         # 3. Crear manómetros CON CALLBACKS
# #         self.blue_box_presion1 = BlueBox(
# #             texto_titulo="MANOMETRO 1",
# #             texto=f"{self.datos_tiempo_real['presion1']} Pa", 
# #             mostrar_boton=False,
# #             on_grafica_click=self.abrir_pagina_grafica
# #         )
        
# #         self.blue_box_presion2 = BlueBox(
# #             texto_titulo="MANOMETRO 2",
# #             texto=f"{self.datos_tiempo_real['presion2']} Pa", 
# #             mostrar_boton=False,
# #             on_grafica_click=self.abrir_pagina_grafica
# #         )
        
# #         self.blue_box_presion3 = BlueBox(
# #             texto_titulo="MANOMETRO 3",
# #             texto=f"{self.datos_tiempo_real['presion3']} Pa", 
# #             mostrar_boton=False,
# #             on_grafica_click=self.abrir_pagina_grafica
# #         )
        
# #         self.blue_boxes = {
# #             'presion1': self.blue_box_presion1,
# #             'presion2': self.blue_box_presion2,
# #             'presion3': self.blue_box_presion3,
# #         }

# #         self.config_container = ConfiguracionContainer(self.page, self.reloj_global)

# #         ################################### PAGINA 1 (UMA) ####################################
# #         self.home_container_1 = ft.Container(
# #             bgcolor=self.color_teal,
# #             border_radius=20,
# #             expand=True,
# #             padding=20,
# #             alignment=ft.alignment.center,
# #             content=ft.Column(
# #                 expand=True,
# #                 controls=[
# #                     self.uma_instance,
# #                 ]
# #             )
# #         )

# #         ################################### PAGINA 2 (MANOMETROS) ####################################
# #         self.location_container_1 = ft.Container(
# #             bgcolor=self.color_teal,
# #             border_radius=20,
# #             expand=True,
# #             padding=20,
# #             content=ft.Column(
# #                 alignment=ft.MainAxisAlignment.START,
# #                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                 expand=True,
# #                 controls=[
# #                     ft.Container(
# #                         expand=True,
# #                         bgcolor=ft.Colors.WHITE,
# #                         border_radius=20,
# #                         alignment=ft.alignment.center,
# #                         padding=20,
# #                         shadow=ft.BoxShadow(
# #                             spread_radius=1,
# #                             blur_radius=10,
# #                             color=ft.Colors.GREY_300,
# #                         ),
# #                         content=ft.Column(
# #                             scroll=ft.ScrollMode.AUTO,
# #                             spacing=30,
# #                             controls=[
# #                                 ft.Row(
# #                                     alignment=ft.MainAxisAlignment.CENTER,
# #                                     vertical_alignment=ft.CrossAxisAlignment.CENTER,
# #                                     spacing=30,
# #                                     controls=[
# #                                         self.blue_box_presion1,
# #                                         self.blue_box_presion2,
# #                                         self.blue_box_presion3,
# #                                     ]
# #                                 )
# #                             ]
# #                         )
# #                     )
# #                 ]
# #             )
# #         )

# #         ################################### PAGINA 3 (ALERTAS) ####################################
# #         self.calendar_container_1 = ft.Container(
# #             bgcolor=self.color_teal,
# #             border_radius=20,
# #             expand=True,
# #             padding=20,
# #             content=ft.Container()
# #         )

# #         ################################### PAGINA 4 (CONFIGURACION) ####################################
# #         self.setting_container_1 = ft.Container(
# #             bgcolor=self.color_teal,
# #             border_radius=20,
# #             expand=True,
# #             padding=20,
# #             content=ft.Column(
# #                 alignment=ft.MainAxisAlignment.CENTER,
# #                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                 expand=True,
# #                 controls=[self.config_container]
# #             )
# #         )

# #         ################################### NUEVOS COMPONENTES PARA PÁGINA DE GRÁFICAS ####################################
        
# #         # Texto para título
# #         self.titulo_grafica_text = ft.Text(
# #             value="Gráfica del Manómetro",
# #             size=24,
# #             weight=ft.FontWeight.BOLD,
# #             color=ft.Colors.BLUE_900
# #         )
        
# #         # Display de presión actual
# #         self.presion_actual_display = ft.Text(
# #             value="-- Pa",
# #             size=20,
# #             weight=ft.FontWeight.BOLD,
# #             color=ft.Colors.GREEN_700
# #         )
        
# #         # Contador de registros
# #         self.contador = ft.Text(
# #             "0 registros",
# #             size=14,
# #             color=ft.Colors.GREY_600
# #         )
        
# #         # Estadísticas
# #         self.presion_promedio_text = ft.Text(
# #             "Promedio: -- Pa",
# #             size=14,
# #             color=ft.Colors.BLUE_600
# #         )
# #         self.presion_maxima_text = ft.Text(
# #             "Máxima: -- Pa",
# #             size=14,
# #             color=ft.Colors.RED_600
# #         )
# #         self.presion_minima_text = ft.Text(
# #             "Mínima: -- Pa",
# #             size=14,
# #             color=ft.Colors.GREEN_600
# #         )
        
# #         # Lista para mostrar historial
# #         self.historial_lista = ft.ListView(
# #             expand=True,
# #             spacing=8,
# #             padding=10
# #         )
        
# #         # Botón para actualizar historial
# #         self.btn_actualizar_historial = ft.IconButton(
# #             icon=ft.Icons.REFRESH,
# #             icon_color=ft.Colors.BLUE_600,
# #             tooltip="Actualizar historial",
# #             on_click=lambda e: self.actualizar_historial_manometro()
# #         )
        
# #         ################################### PÁGINA 5 (GRÁFICAS) ####################################
# #         self.grafica_container = ft.Container(
# #             bgcolor=self.color_teal,
# #             border_radius=20,
# #             expand=True,
# #             padding=20,
# #             content=ft.Column(
# #                 expand=True,
# #                 spacing=20,
# #                 controls=[
# #                     # CABECERA
# #                     ft.Container(
# #                         padding=ft.padding.symmetric(vertical=10, horizontal=15),
# #                         bgcolor=ft.Colors.WHITE,
# #                         border_radius=10,
# #                         shadow=ft.BoxShadow(
# #                             spread_radius=1,
# #                             blur_radius=5,
# #                             color=ft.Colors.GREY_300,
# #                         ),
# #                         content=ft.Row(
# #                             alignment=ft.MainAxisAlignment.START,
# #                             vertical_alignment=ft.CrossAxisAlignment.CENTER,
# #                             spacing=20,
# #                             controls=[
# #                                 ft.IconButton(
# #                                     icon=ft.Icons.ARROW_BACK,
# #                                     icon_color=ft.Colors.BLUE_700,
# #                                     icon_size=28,
# #                                     on_click=lambda e: self.change_page_manual(1),
# #                                     tooltip="Volver a Manómetros"
# #                                 ),
# #                                 self.titulo_grafica_text,
# #                                 self.btn_actualizar_historial
# #                             ]
# #                         )
# #                     ),
                    
# #                     # CONTENIDO PRINCIPAL
# #                     ft.Container(
# #                         expand=True,
# #                         bgcolor=ft.Colors.WHITE,
# #                         border_radius=15,
# #                         padding=25,
# #                         shadow=ft.BoxShadow(
# #                             spread_radius=1,
# #                             blur_radius=10,
# #                             color=ft.Colors.GREY_300,
# #                         ),
# #                         content=ft.Column(
# #                             expand=True,
# #                             spacing=25,
# #                             controls=[
# #                                 # Información del manómetro
# #                                 ft.Container(
# #                                     padding=15,
# #                                     bgcolor=ft.Colors.BLUE_50,
# #                                     border_radius=10,
# #                                     content=ft.Column(
# #                                         spacing=10,
# #                                         controls=[
# #                                             ft.Row(
# #                                                 spacing=10,
# #                                                 controls=[
# #                                                     ft.Text("Presión actual:", size=16, color=ft.Colors.GREY_600),
# #                                                     self.presion_actual_display,
# #                                                     ft.VerticalDivider(width=20, color=ft.Colors.GREY_300),
# #                                                     ft.Text("Total registros:", size=16, color=ft.Colors.GREY_600),
# #                                                     self.contador,
# #                                                 ]
# #                                             ),
# #                                             ft.Divider(height=1, color=ft.Colors.GREY_300),
# #                                             ft.Row(
# #                                                 spacing=20,
# #                                                 controls=[
# #                                                     self.presion_promedio_text,
# #                                                     self.presion_maxima_text,
# #                                                     self.presion_minima_text
# #                                                 ]
# #                                             )
# #                                         ]
# #                                     )
# #                                 ),
                                
# #                                 # Encabezado del historial
# #                                 ft.Container(
# #                                     padding=10,
# #                                     bgcolor=ft.Colors.GREY_50,
# #                                     border_radius=10,
# #                                     content=ft.Row(
# #                                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                                         controls=[
# #                                             ft.Text("Historial de Registros", 
# #                                                 size=18, weight=ft.FontWeight.BOLD),
# #                                             ft.Text("Mostrando registros del historial principal", 
# #                                                 size=12, color=ft.Colors.GREY_600),
# #                                         ]
# #                                     )
# #                                 ),
                                
# #                                 # Lista de historial
# #                                 ft.Container(
# #                                     expand=True,
# #                                     border=ft.border.all(1, ft.Colors.GREY_300),
# #                                     border_radius=10,
# #                                     padding=10,
# #                                     content=self.historial_lista
# #                                 ),
                                
# #                                 # Leyenda
# #                                 ft.Container(
# #                                     padding=10,
# #                                     content=ft.Row(
# #                                         spacing=15,
# #                                         alignment=ft.MainAxisAlignment.CENTER,
# #                                         controls=[
# #                                             ft.Row([
# #                                                 ft.Container(width=12, height=12, 
# #                                                         bgcolor=ft.Colors.BLUE_50, 
# #                                                         border_radius=6),
# #                                                 ft.Text("Registros automáticos", size=10),
# #                                             ]),
# #                                             ft.Row([
# #                                                 ft.Container(width=12, height=12, 
# #                                                         bgcolor=ft.Colors.GREEN_50, 
# #                                                         border_radius=6),
# #                                                 ft.Text("Registros manuales", size=10),
# #                                             ]),
# #                                             ft.Row([
# #                                                 ft.Container(width=12, height=12, 
# #                                                         bgcolor=ft.Colors.ORANGE_50, 
# #                                                         border_radius=6),
# #                                                 ft.Text("Registros con alerta", size=10),
# #                                             ]),
# #                                         ]
# #                                     )
# #                                 )
# #                             ]
# #                         )
# #                     )
# #                 ]
# #             )
# #         )

# #         # Lista de todas las páginas
# #         self.container_list_1 = [
# #             self.home_container_1,      # índice 0: UMA
# #             self.location_container_1,  # índice 1: Manómetros  
# #             self.calendar_container_1,  # índice 2: Alertas
# #             self.setting_container_1,   # índice 3: Configuración
# #             self.grafica_container      # índice 4: Gráficas
# #         ]
        
# #         self.container_1 = ft.Container(
# #             content=self.container_list_1[0], 
# #             expand=True,
# #             animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
# #         )

# #         # ========== BARRA DE NAVEGACIÓN PROFESIONAL ==========
# #         self.btn_connect = self._crear_boton_navegacion_profesional("UMA", ft.Icons.MONITOR_HEART, 0)
# #         self.btn_connect2 = self._crear_boton_navegacion_profesional("Manómetros", ft.Icons.SPEED, 1)
# #         self.btn_connect3 = self._crear_boton_navegacion_profesional("Alertas", ft.Icons.NOTIFICATIONS, 2)
# #         self.btn_connect4 = self._crear_boton_navegacion_profesional("Configuración", ft.Icons.SETTINGS, 3)

# #         # Barra lateral de navegación
# #         self.navigation_container = ft.Container(
# #             col=2,
# #             expand=True,
# #             bgcolor=ft.Colors.WHITE,
# #             border_radius=0,
# #             border=ft.border.only(right=ft.border.BorderSide(1, self.color_borde)),
# #             padding=ft.padding.symmetric(vertical=30, horizontal=20),
# #             shadow=ft.BoxShadow(
# #                 spread_radius=0,
# #                 blur_radius=20,
# #                 color="rgba(39, 245, 180, 0.08)",
# #                 offset=ft.Offset(5, 0)
# #             ),
# #             content=ft.Column(
# #                 alignment=ft.MainAxisAlignment.START,
# #                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                 expand=True,
# #                 spacing=15,
# #                 controls=[
# #                     # Logo y nombre
# #                     ft.Container(
# #                         padding=ft.padding.only(bottom=30),
# #                         content=ft.Column(
# #                             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                             spacing=10,
# #                             controls=[
# #                                 ft.Container(
# #                                     width=60,
# #                                     height=60,
# #                                     border_radius=15,
# #                                     bgcolor=self.color_primario,
# #                                     alignment=ft.alignment.center,
# #                                     shadow=ft.BoxShadow(
# #                                         spread_radius=0,
# #                                         blur_radius=15,
# #                                         color="rgba(39, 245, 180, 0.15)",
# #                                     ),
# #                                     content=ft.Icon(
# #                                         ft.Icons.MONITOR_HEART,
# #                                         color=ft.Colors.WHITE,
# #                                         size=30
# #                                     )
# #                                 ),
# #                                 ft.Column(
# #                                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                                     spacing=2,
# #                                     controls=[
# #                                         ft.Text(
# #                                             "Sistema de",
# #                                             size=14,
# #                                             weight=ft.FontWeight.BOLD,
# #                                             color=self.color_texto
# #                                         ),
# #                                         ft.Text(
# #                                             "Monitoreo",
# #                                             size=14,
# #                                             weight=ft.FontWeight.BOLD,
# #                                             color=self.color_primario
# #                                         )
# #                                     ]
# #                                 )
# #                             ]
# #                         )
# #                     ),
                    
# #                     ft.Divider(height=20, color=self.color_borde),
                    
# #                     # Botones de navegación
# #                     self.btn_connect,
# #                     self.btn_connect2,
# #                     self.btn_connect3,
# #                     self.btn_connect4,
                    
# #                     ft.Divider(height=30, color=self.color_borde),
                    
# #                     # Estado del sistema
# #                     ft.Container(
# #                         padding=15,
# #                         bgcolor=f"{self.color_primario}08",
# #                         border_radius=10,
# #                         content=ft.Column(
# #                             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                             spacing=8,
# #                             controls=[
# #                                 ft.Row(
# #                                     spacing=8,
# #                                     controls=[
# #                                         ft.Container(
# #                                             width=10,
# #                                             height=10,
# #                                             border_radius=5,
# #                                             bgcolor=self.color_primario
# #                                         ),
# #                                         ft.Text(
# #                                             "Sistema Activo",
# #                                             size=12,
# #                                             weight=ft.FontWeight.W_600,
# #                                             color=self.color_texto
# #                                         )
# #                                     ]
# #                                 ),
# #                                 ft.Text(
# #                                     datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
# #                                     size=11,
# #                                     color=self.color_texto_secundario
# #                                 )
# #                             ]
# #                         )
# #                     )
# #                 ]
# #             )
# #         )

# #         # Área principal de contenido
# #         self.frame_2 = ft.Container(
# #             col=10,
# #             alignment=ft.alignment.center,
# #             bgcolor=self.color_teal,
# #             expand=True,
# #             content=ft.Column(
# #                 expand=True,
# #                 controls=[
# #                     self.container_1,
# #                 ]
# #             )   
# #         )
        
# #         # Layout principal
# #         self.resp_container = ft.ResponsiveRow(
# #             vertical_alignment=ft.CrossAxisAlignment.STRETCH,
# #             controls=[
# #                 self.navigation_container,
# #                 self.frame_2,
# #             ]
# #         )

# #         self.iniciar_home_random()
# #         self.actualizar_colores_botones(0)

# #     def redondear_entero_desde_6(self, valor):
# #         """Redondea hacia arriba desde 0.6"""
# #         parte_entera = int(valor)
# #         decimal = valor - parte_entera
# #         return parte_entera + 1 if decimal >= 0.6 else parte_entera
    
# #     def generar_datos_random(self):
# #         """Genera datos aleatorios con verificación de alertas"""
# #         temp_original = random.uniform(15, 35)
# #         hum_original = random.uniform(30, 90)
# #         pres1_original = random.uniform(80, 110)
# #         pres2_original = random.uniform(80, 110)
# #         pres3_original = random.uniform(80, 110)

# #         temp = self.redondear_entero_desde_6(temp_original)
# #         hum = self.redondear_entero_desde_6(hum_original)
# #         pres1 = self.redondear_entero_desde_6(pres1_original)
# #         pres2 = self.redondear_entero_desde_6(pres2_original)
# #         pres3 = self.redondear_entero_desde_6(pres3_original)

# #         self.datos_tiempo_real = {
# #             'temperatura': temp,
# #             'humedad': hum, 
# #             'presion1': pres1,
# #             'presion2': pres2,
# #             'presion3': pres3,
# #         }

# #         # Actualizar manómetros
# #         for key, box in self.blue_boxes.items():
# #             if hasattr(box, 'actualizar_valor'):
# #                 valor = self.datos_tiempo_real[key]
# #                 box.actualizar_valor(f"{valor} Pa")
        
# #         return {"presion1": pres1, "presion2": pres2, "presion3": pres3, "temperatura": temp, "humedad": hum}

# #     def iniciar_home_random(self):
# #         """Inicia la generación aleatoria de datos"""
# #         def loop():
# #             while True:
# #                 datos = self.generar_datos_random()
                
# #                 def actualizar():
# #                     # Actualiza los controles que UMA usa
# #                     self.txt_temp_home.value = f"{datos['temperatura']} °C"
# #                     self.txt_hum_home.value = f"{datos['humedad']} %"
# #                     self.txt_pres_home.value = f"{datos['presion1']} Pa"
                    
# #                     # Actualizar también la página de gráficas si estamos en ella
# #                     if (hasattr(self, 'manometro_activo') and 
# #                         hasattr(self, 'presion_actual_display') and
# #                         self.container_1.content == self.grafica_container):
                        
# #                         if self.manometro_numero == 1:
# #                             self.presion_actual_display.value = f"{self.datos_tiempo_real['presion1']} Pa"
# #                         elif self.manometro_numero == 2:
# #                             self.presion_actual_display.value = f"{self.datos_tiempo_real['presion2']} Pa"
# #                         elif self.manometro_numero == 3:
# #                             self.presion_actual_display.value = f"{self.datos_tiempo_real['presion3']} Pa"
                    
# #                     self.page.update()
                
# #                 self.page.run_thread(actualizar)
# #                 time.sleep(2)
        
# #         threading.Thread(target=loop, daemon=True).start()

# #     def change_page_manual(self, index):
# #         """Cambia entre páginas de la aplicación"""
# #         self.container_1.content = self.container_list_1[index]
# #         self.actualizar_colores_botones(index)
        
# #         # Si estamos entrando a la página de gráficas, actualizar el historial
# #         if index == 4 and self.manometro_activo and self.manometro_numero:
# #             self.actualizar_historial_manometro()
        
# #         # Actualizar estado de la página de Alertas
# #         if index == 2:
# #             self.en_pagina_alertas = True
# #             if self.notificacion_badge is not None:
# #                 self.notificacion_badge.visible = False
# #                 try:
# #                     self.notificacion_badge.update()
# #                 except:
# #                     pass
# #         else:
# #             self.en_pagina_alertas = False
# #             self.actualizar_contador_alertas()
        
# #         if self.alertas_view is not None:
# #             if index == 2:
# #                 if hasattr(self.alertas_view, 'entrar_a_pagina'):
# #                     self.alertas_view.entrar_a_pagina()
# #             else:
# #                 if hasattr(self.alertas_view, 'salir_de_pagina'):
# #                     self.alertas_view.salir_de_pagina()

# #         self.page.update()
    
# #     def actualizar_colores_botones(self, index_activo):
# #         """Actualiza los colores y formas de los botones de navegación"""
# #         botones = [self.btn_connect, self.btn_connect2, self.btn_connect3, self.btn_connect4]
        
# #         for i, btn in enumerate(botones):
# #             if i == index_activo:
# #                 # Botón activo
# #                 btn.bgcolor = self.color_primario
# #                 btn.border = ft.border.all(1, self.color_primario)
                
# #                 contenido = btn.content
                
# #                 if i == 2 and isinstance(contenido, ft.Stack):
# #                     boton_container = contenido.controls[0]
# #                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
# #                         row_controls = boton_container.content.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = ft.Colors.WHITE
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = ft.Colors.WHITE
# #                 else:
# #                     if isinstance(contenido, ft.Row):
# #                         row_controls = contenido.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = ft.Colors.WHITE
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = ft.Colors.WHITE
# #                 btn.scale = ft.Scale(1.0)
# #             else:
# #                 # Botones inactivos
# #                 btn.bgcolor = ft.Colors.WHITE
# #                 btn.border = ft.border.all(1, self.color_borde)
                
# #                 contenido = btn.content
                
# #                 if i == 2 and isinstance(contenido, ft.Stack):
# #                     boton_container = contenido.controls[0]
# #                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
# #                         row_controls = boton_container.content.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_texto_secundario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_texto
# #                 else:
# #                     if isinstance(contenido, ft.Row):
# #                         row_controls = contenido.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_texto_secundario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_texto
# #                 btn.scale = ft.Scale(1.0)
        
# #         for btn in botones:
# #             try:
# #                 btn.update()
# #             except:
# #                 pass

# #     # ========== MÉTODOS PARA LA PÁGINA DE GRÁFICAS ==========
    
# #     def abrir_pagina_grafica(self, titulo_manometro):
# #         """Abre la página de gráficas para un manómetro específico"""
# #         print(f"Abriendo gráfica para: {titulo_manometro}")
        
# #         self.manometro_activo = titulo_manometro
        
# #         # Determinar número de manómetro
# #         if "MANOMETRO 1" in titulo_manometro:
# #             self.manometro_numero = 1
# #             datos = self.datos_tiempo_real['presion1']
# #         elif "MANOMETRO 2" in titulo_manometro:
# #             self.manometro_numero = 2
# #             datos = self.datos_tiempo_real['presion2']
# #         elif "MANOMETRO 3" in titulo_manometro:
# #             self.manometro_numero = 3
# #             datos = self.datos_tiempo_real['presion3']
# #         else:
# #             self.manometro_numero = None
# #             datos = 0
        
# #         # Actualizar título
# #         self.titulo_grafica_text.value = f"Historial: {titulo_manometro}"
        
# #         # Actualizar display
# #         self.presion_actual_display.value = f"{datos} Pa"
        
# #         # Cambiar a la página de gráficas
# #         self.change_page_manual(4)
        
# #         # Actualizar historial
# #         self.actualizar_historial_manometro()
        
# #         print(f"✓ Página de historial abierta para {titulo_manometro}")
# #         print(f"  Presión actual: {datos} Pa")
# #         print(f"  Número de manómetro: {self.manometro_numero}")
    
# #     def actualizar_historial_manometro(self, e=None):
# #         """Actualiza la lista de historial para el manómetro activo"""
# #         if not self.manometro_activo or not self.manometro_numero:
# #             return
        
# #         # Obtener registros del manómetro desde el historial principal
# #         registros = self.reloj_global.obtener_registros_por_manometro(self.manometro_numero)
        
# #         # Actualizar contador
# #         self.contador.value = f"{len(registros)} registros"
        
# #         # Calcular estadísticas
# #         if registros:
# #             presiones = [r['presion'] for r in registros]
# #             promedio = sum(presiones) / len(presiones)
# #             maxima = max(presiones)
# #             minima = min(presiones)
            
# #             self.presion_promedio_text.value = f"Promedio: {promedio:.1f} Pa"
# #             self.presion_maxima_text.value = f"Máxima: {maxima} Pa"
# #             self.presion_minima_text.value = f"Mínima: {minima} Pa"
# #         else:
# #             self.presion_promedio_text.value = "Promedio: -- Pa"
# #             self.presion_maxima_text.value = "Máxima: -- Pa"
# #             self.presion_minima_text.value = "Mínima: -- Pa"
        
# #         # Limpiar lista actual
# #         self.historial_lista.controls.clear()
        
# #         # Mostrar en orden inverso (más reciente primero)
# #         for registro in registros[:50]:  # Mostrar solo los últimos 50 registros
# #             # Determinar color según tipo
# #             if "automatico" in registro['tipo']:
# #                 color_fondo = ft.Colors.BLUE_50
# #                 tipo_texto = "AUTO"
# #             elif "manual" in registro['tipo']:
# #                 color_fondo = ft.Colors.GREEN_50
# #                 tipo_texto = "MANUAL"
# #             else:
# #                 color_fondo = ft.Colors.GREY_50
# #                 tipo_texto = "OTRO"
            
# #             # Verificar si hubo alerta en este registro
# #             tiene_alerta = registro['presion'] > 108
            
# #             # Crear tarjeta para cada registro
# #             tarjeta = ft.Card(
# #                 elevation=2,
# #                 content=ft.Container(
# #                     padding=15,
# #                     bgcolor=ft.Colors.ORANGE_50 if tiene_alerta else ft.Colors.WHITE,
# #                     content=ft.Column(
# #                         spacing=5,
# #                         controls=[
# #                             ft.Row(
# #                                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                                 controls=[
# #                                     ft.Text(
# #                                         f"Presión: {registro['presion']} Pa",
# #                                         size=16,
# #                                         weight=ft.FontWeight.BOLD,
# #                                         color=ft.Colors.RED_700 if tiene_alerta else ft.Colors.BLUE_700
# #                                     ),
# #                                     ft.Row(
# #                                         spacing=5,
# #                                         controls=[
# #                                             ft.Container(
# #                                                 padding=ft.padding.symmetric(horizontal=8, vertical=4),
# #                                                 bgcolor=color_fondo,
# #                                                 border_radius=5,
# #                                                 content=ft.Text(
# #                                                     tipo_texto,
# #                                                     size=10,
# #                                                     weight=ft.FontWeight.BOLD
# #                                                 )
# #                                             ),
# #                                             ft.Container(
# #                                                 padding=ft.padding.symmetric(horizontal=8, vertical=4),
# #                                                 bgcolor=ft.Colors.RED_100 if tiene_alerta else ft.Colors.GREEN_100,
# #                                                 border_radius=5,
# #                                                 content=ft.Text(
# #                                                     "ALERTA" if tiene_alerta else "NORMAL",
# #                                                     size=10,
# #                                                     weight=ft.FontWeight.BOLD,
# #                                                     color=ft.Colors.RED_700 if tiene_alerta else ft.Colors.GREEN_700
# #                                                 )
# #                                             ) if tiene_alerta else ft.Container()
# #                                         ]
# #                                     )
# #                                 ]
# #                             ),
# #                             ft.Row(
# #                                 controls=[
# #                                     ft.Icon(ft.Icons.CALENDAR_TODAY, size=14, color=ft.Colors.GREY_500),
# #                                     ft.Text(registro['fecha'], size=12, color=ft.Colors.GREY_600),
# #                                     ft.VerticalDivider(width=10),
# #                                     ft.Icon(ft.Icons.ACCESS_TIME, size=14, color=ft.Colors.GREY_500),
# #                                     ft.Text(registro['hora'], size=12, color=ft.Colors.GREY_600),
# #                                     ft.VerticalDivider(width=10),
# #                                     ft.Icon(ft.Icons.THERMOSTAT, size=14, color=ft.Colors.GREY_500),
# #                                     ft.Text(f"{registro.get('temperatura', 0)}°C", size=12, color=ft.Colors.GREY_600),
# #                                     ft.VerticalDivider(width=10),
# #                                     ft.Icon(ft.Icons.WATER_DROP, size=14, color=ft.Colors.GREY_500),
# #                                     ft.Text(f"{registro.get('humedad', 0)}%", size=12, color=ft.Colors.GREY_600),
# #                                 ]
# #                             ),
# #                             ft.Text(
# #                                 f"Fuente: {registro.get('fuente', 'Desconocido')}",
# #                                 size=11,
# #                                 color=ft.Colors.GREY_500,
# #                                 italic=True
# #                             )
# #                         ]
# #                     )
# #                 )
# #             )
            
# #             self.historial_lista.controls.append(tarjeta)
        
# #         # Si no hay registros, mostrar mensaje
# #         if not registros:
# #             self.historial_lista.controls.append(
# #                 ft.Container(
# #                     padding=20,
# #                     alignment=ft.alignment.center,
# #                     content=ft.Column(
# #                         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                         spacing=10,
# #                         controls=[
# #                             ft.Icon(ft.Icons.HISTORY, size=48, color=ft.Colors.GREY_400),
# #                             ft.Text(
# #                                 "No hay registros históricos para este manómetro",
# #                                 size=16,
# #                                 color=ft.Colors.GREY_500
# #                             ),
# #                             ft.Text(
# #                                 "Los registros aparecerán cuando se ejecuten alarmas\n"
# #                                 "o se hagan registros manuales desde la página UMA",
# #                                 size=12,
# #                                 color=ft.Colors.GREY_400,
# #                                 text_align=ft.TextAlign.CENTER
# #                             )
# #                         ]
# #                     )
# #                 )
# #             )
        
# #         # Actualizar todos los componentes
# #         try:
# #             self.historial_lista.update()
# #             self.contador.update()
# #             self.presion_promedio_text.update()
# #             self.presion_maxima_text.update()
# #             self.presion_minima_text.update()
# #         except:
# #             pass

# #     def will_unmount(self):
# #         """Detener el reloj global al cerrar la app"""
# #         self.reloj_global.detener()


# # def main(page: ft.Page):
# #     page.title = "Sistema de Monitoreo Inteligente"
# #     page.window.width = 1400
# #     page.window.height = 750
# #     page.window.resizable = True
# #     page.horizontal_alignment = "center"
# #     page.vertical_alignment = "center"
# #     page.theme_mode = ft.ThemeMode.LIGHT
# #     page.window.bgcolor = ft.Colors.WHITE
# #     page.padding = 0

# #     ui = UI(page)
# #     page.add(ui)

# # if __name__ == "__main__":
# #     ft.app(target=main)

































# # CON GRAFICA
# # import flet as ft
# # import threading
# # import time
# # import datetime
# # import json
# # import os
# # import random
# # from cajaAzul import BlueBox
# # from configuracion import ConfiguracionContainer
# # from excel5 import ExcelUnicoArchivo
# # from alertas import SistemaAlertas, AlertasView
# # from paguina1 import UMA

# # class RelojGlobal:
# #     def __init__(self):
# #         self.horas_registradas = []
# #         self.archivo_horas = "horas.json"
# #         self.historial_registros = []
# #         self.archivo_historial = "historial_registros.json"
# #         self.reloj_activo = True
# #         self.ultima_ejecucion = {}
# #         self.callbacks = []
# #         self.historial_callbacks = []
        
# #         # Cargar horas guardadas
# #         self.cargar_horas()
# #         self.cargar_historial()
# #         self.iniciar()

# #     def agregar_callback(self, callback):
# #         """Agrega una función que se ejecutará cuando suene una alarma"""
# #         self.callbacks.append(callback)
    
# #     def agregar_callback_historial(self, callback):
# #         """Agrega una función que se ejecutará cuando se agregue un nuevo registro al historial"""
# #         self.historial_callbacks.append(callback)

# #     def cargar_horas(self):
# #         """Carga las horas desde archivo JSON"""
# #         if os.path.exists(self.archivo_horas):
# #             try:
# #                 with open(self.archivo_horas, "r") as file:
# #                     datos = json.load(file)
# #                     self.horas_registradas = [
# #                         datetime.datetime.strptime(h, "%H:%M").time()
# #                         for h in datos
# #                     ]
# #                 print(f"RelojGlobal: Horas cargadas: {[h.strftime('%I:%M %p') for h in self.horas_registradas]}")
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error cargando horas: {e}")
# #                 self.horas_registradas = []
    
# #     def cargar_historial(self):
# #         """Carga el historial desde archivo JSON"""
# #         if os.path.exists(self.archivo_historial):
# #             try:
# #                 with open(self.archivo_historial, "r") as file:
# #                     self.historial_registros = json.load(file)
# #                 print(f"RelojGlobal: Historial cargado ({len(self.historial_registros)} registros)")
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error cargando historial: {e}")
# #                 self.historial_registros = []
# #         else:
# #             self.guardar_historial()

# #     def guardar_horas(self):
# #         """Guarda las horas en archivo JSON"""
# #         try:
# #             datos = [h.strftime("%H:%M") for h in self.horas_registradas]
# #             with open(self.archivo_horas, "w") as file:
# #                 json.dump(datos, file)
# #         except Exception as e:
# #             print(f"RelojGlobal: Error guardando horas: {e}")
    
# #     def guardar_historial(self):
# #         """Guarda el historial en archivo JSON"""
# #         try:
# #             if len(self.historial_registros) > 50:
# #                 self.historial_registros = self.historial_registros[-50:]
            
# #             with open(self.archivo_historial, "w") as file:
# #                 json.dump(self.historial_registros, file, indent=2)
# #         except Exception as e:
# #             print(f"RelojGlobal: Error guardando historial: {e}")

# #     def agregar_hora(self, hora_time):
# #         """Agrega una hora a la lista global"""
# #         if hora_time not in self.horas_registradas:
# #             self.horas_registradas.append(hora_time)
# #             self.guardar_horas()
# #             print(f"RelojGlobal: Hora agregada: {hora_time.strftime('%I:%M %p')}")
# #             return True
# #         return False

# #     def eliminar_hora(self, hora_time):
# #         """Elimina una hora de la lista global"""
# #         if hora_time in self.horas_registradas:
# #             self.horas_registradas.remove(hora_time)
# #             self.guardar_horas()
# #             print(f"RelojGlobal: Hora eliminada: {hora_time.strftime('%I:%M %p')}")
# #             return True
# #         return False
    
# #     def agregar_al_historial(self, datos, tipo="registro_automatico", fuente="Reloj Global"):
# #         """Agrega un registro al historial"""
# #         registro = {
# #             "fecha": datetime.datetime.now().strftime("%d/%m/%y"),
# #             "hora": datetime.datetime.now().strftime("%H:%M"),
# #             "datos": datos,
# #             "tipo": tipo,
# #             "fuente": fuente
# #         }
# #         self.historial_registros.append(registro)
# #         self.guardar_historial()
        
# #         # Notificar a todos los callbacks
# #         for callback in self.historial_callbacks:
# #             try:
# #                 callback()
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error en callback de historial: {e}")
        
# #         return registro
    
# #     def obtener_registros_por_manometro(self, manometro_numero, limite=50):
# #         """
# #         Obtiene todos los registros históricos para un manómetro específico.
# #         manometro_numero: 1, 2 o 3
# #         limite: cantidad máxima de registros a retornar
# #         """
# #         registros_manometro = []
        
# #         # Filtrar registros para este manómetro
# #         for registro in reversed(self.historial_registros):  # Más recientes primero
# #             if 'datos' in registro:
# #                 datos = registro['datos']
# #                 # Extraer la presión del manómetro específico
# #                 clave_presion = f'presion{manometro_numero}'
# #                 if clave_presion in datos:
# #                     registro_manometro = {
# #                         'fecha': registro['fecha'],
# #                         'hora': registro['hora'],
# #                         'presion': datos[clave_presion],
# #                         'tipo': registro.get('tipo', 'desconocido'),
# #                         'fuente': registro.get('fuente', 'desconocido')
# #                     }
# #                     registros_manometro.append(registro_manometro)
            
# #             # Limitar cantidad de registros
# #             if len(registros_manometro) >= limite:
# #                 break
        
# #         return registros_manometro

# #     def limpiar_historial(self):
# #         """Limpia todo el historial"""
# #         self.historial_registros = []
# #         self.guardar_historial()
# #         print("RelojGlobal: Historial limpiado")
        
# #         # Notificar a los callbacks
# #         for callback in self.historial_callbacks:
# #             try:
# #                 callback()
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error en callback de limpieza: {e}")

# #     def iniciar(self):
# #         """Inicia el reloj global en un hilo separado"""
# #         if not hasattr(self, 'thread') or not self.thread.is_alive():
# #             self.thread = threading.Thread(target=self._loop, daemon=True)
# #             self.thread.start()
# #             print("RelojGlobal: Iniciado")

# #     def _loop(self):
# #         """Loop principal del reloj"""
# #         while self.reloj_activo:
# #             try:
# #                 ahora = datetime.datetime.now()
                
# #                 for hora_obj in self.horas_registradas:
# #                     hora_actual_minuto = ahora.strftime("%I:%M %p")
# #                     segundos = ahora.strftime("%S")
# #                     hora_objetivo_str = hora_obj.strftime("%I:%M %p")

# #                     if hora_actual_minuto == hora_objetivo_str and segundos == "00":
# #                         h_obj = datetime.datetime.combine(ahora.date(), hora_obj)
# #                         clave = h_obj.strftime("%Y-%m-%d %H:%M")

# #                         if clave not in self.ultima_ejecucion:
# #                             self.ultima_ejecucion[clave] = True
# #                             self._ejecutar_alarma(hora_objetivo_str)
# #                             print(f"RelojGlobal: ✓ Alarma: {hora_objetivo_str}")
                
# #                 hoy = datetime.datetime.now().date()
# #                 claves_a_eliminar = [k for k in self.ultima_ejecucion 
# #                                     if datetime.datetime.strptime(k.split(" ")[0], "%Y-%m-%d").date() < hoy]
# #                 for k in claves_a_eliminar:
# #                     del self.ultima_ejecucion[k]

# #                 time.sleep(1)
                
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error en loop: {e}")
# #                 time.sleep(1)

# #     def _ejecutar_alarma(self, hora):
# #         """Ejecuta todos los callbacks registrados"""
# #         for callback in self.callbacks:
# #             try:
# #                 callback(hora)
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error en callback: {e}")

# #     def detener(self):
# #         """Detiene el reloj global"""
# #         self.reloj_activo = False


# # class UI(ft.Container):
# #     def __init__(self, page):
# #         super().__init__(expand=True)
# #         self.page = page
        
# #         # COLORES PARA LA BARRA DE NAVEGACIÓN
# #         self.color_primario = "#27F5B4"  # Verde agua
# #         self.color_fondo = "#FFFFFF"  # Blanco
# #         self.color_texto = "#2C3E50"  # Azul oscuro
# #         self.color_texto_secundario = "#6C757D"  # Gris
# #         self.color_borde = "#E9ECEF"  # Gris claro para bordes
        
# #         # Datos en tiempo real (manteniendo los originales)
# #         self.datos_tiempo_real = {
# #             'temperatura': 0,
# #             'humedad': 0, 
# #             'presion1': 0,
# #             'presion2': 0,
# #             'presion3': 0,
# #         }

# #         self.excel_manager = ExcelUnicoArchivo()
# #         self.bandera_excel = self.excel_manager.get_bandera_archivo()
        
# #         self.reloj_global = RelojGlobal()
# #         self.sistema_alertas = SistemaAlertas()
# #         self.alertas_view = None
        
# #         # Variable para el badge de notificaciones
# #         self.notificacion_badge = None
# #         # Variable para saber si estamos en la página de Alertas
# #         self.en_pagina_alertas = False
        
# #         # Variables para gráficas
# #         self.manometro_activo = None
# #         self.manometro_numero = None
# #         self.grafica_chart = None
# #         self.lista_historial_grafica = None
# #         self.titulo_grafica_text = None

# #         self.banner = ft.Banner(
# #             bgcolor=ft.Colors.AMBER_100,
# #             leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
# #             content=ft.Text(
# #                 "Sistema de monitoreo iniciado",
# #                 color=ft.Colors.BLACK,
# #             ),
# #             actions=[
# #                 ft.TextButton("OK", on_click=self.cerrar_banner)
# #             ],
# #         )
# #         self.page.controls.append(self.banner)

# #         if not self.bandera_excel:
# #             print("⚠️ Main: No se encontró archivo Excel, mostrando banner...")
# #             self.mostrar_banner_inicio()
# #         else:
# #             self.reloj_global.agregar_callback(self._on_alarma)
# #             print("✅ Main: Archivo Excel encontrado")

# #         self.color_teal = ft.Colors.GREY_300

# #         self._initialize_ui_components()
# #         self.content = self.resp_container
        
# #         self.inicializar_alertas_view()

# #     def _crear_boton_navegacion_profesional(self, texto, icono, index):
# #         """Crea un botón de navegación con diseño profesional y badge de notificaciones"""
        
# #         # Contenedor para el contenido del botón (icono + texto)
# #         contenido_boton = ft.Row(
# #             alignment=ft.MainAxisAlignment.CENTER,
# #             vertical_alignment=ft.CrossAxisAlignment.CENTER,
# #             spacing=15,
# #             controls=[
# #                 ft.Icon(icono, color=self.color_texto_secundario, size=22),
# #                 ft.Text(
# #                     texto, 
# #                     color=self.color_texto,
# #                     weight=ft.FontWeight.W_600,
# #                     size=14
# #                 )
# #             ]
# #         )
        
# #         # Crear el botón principal
# #         boton_principal = ft.Container(
# #             width=160,
# #             height=60,
# #             bgcolor=ft.Colors.WHITE,
# #             border_radius=10,
# #             border=ft.border.all(1, self.color_borde),
# #             alignment=ft.alignment.center,
# #             clip_behavior=ft.ClipBehavior.HARD_EDGE,
# #             animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
# #             on_hover=lambda e: self._on_hover_boton_nav(e, index),
# #             on_click=lambda e: self.change_page_manual(index),
# #         )
        
# #         # Si es el botón de Alertas, agregar el badge
# #         if index == 2:
# #             # Crear el badge
# #             badge = ft.Container(
# #                 width=20,
# #                 height=20,
# #                 border_radius=10,
# #                 bgcolor=ft.Colors.RED_600,
# #                 alignment=ft.alignment.center,
# #                 visible=False,
# #                 content=ft.Text(
# #                     "0",
# #                     size=10,
# #                     color=ft.Colors.WHITE,
# #                     weight=ft.FontWeight.BOLD
# #                 )
# #             )
            
# #             # Guardar referencia al badge
# #             self.notificacion_badge = badge
            
# #             # Crear el Stack con el botón y el badge
# #             stack_content = ft.Stack(
# #                 controls=[
# #                     # El contenido del botón (centrado)
# #                     ft.Container(
# #                         content=contenido_boton,
# #                         alignment=ft.alignment.center,
# #                         width=160,
# #                         height=60,
# #                     ),
# #                     # El badge posicionado en la esquina superior derecha
# #                     badge
# #                 ],
# #                 width=170,
# #                 height=65,
# #             )
            
# #             # Configurar el badge para que esté en la esquina superior derecha
# #             badge.top = 0
# #             badge.right = 0
            
# #             boton_principal.content = stack_content
# #             return boton_principal
# #         else:
# #             # Para otros botones, contenido simple
# #             boton_principal.content = contenido_boton
# #             return boton_principal

# #     def _on_hover_boton_nav(self, e, index):
# #         """Maneja el hover de los botones de navegación"""
# #         ctrl = e.control
# #         is_hover = (e.data == "true" or e.data is True)
        
# #         # Determinar qué botón está activo
# #         botones = [self.btn_connect, self.btn_connect2, self.btn_connect3, self.btn_connect4]
# #         index_activo = self.container_list_1.index(self.container_1.content) if self.container_1.content in self.container_list_1 else 0
        
# #         # Si no es el botón activo
# #         if index != index_activo:
# #             if is_hover:
# #                 ctrl.bgcolor = f"{self.color_primario}10"  # 10% de opacidad
# #                 ctrl.border = ft.border.all(1, self.color_primario)
# #                 ctrl.scale = ft.Scale(1.02)
                
# #                 # Obtener el contenido del botón (diferente para botón con Stack)
# #                 contenido = ctrl.content
                
# #                 # Si es el botón de Alertas (con Stack)
# #                 if index == 2 and isinstance(contenido, ft.Stack):
# #                     # El contenido está en el primer elemento del Stack (índice 0)
# #                     boton_container = contenido.controls[0]
# #                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
# #                         row_controls = boton_container.content.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_primario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_primario
# #                 else:
# #                     # Para botones normales
# #                     if isinstance(contenido, ft.Row):
# #                         row_controls = contenido.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_primario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_primario
# #             else:
# #                 ctrl.bgcolor = ft.Colors.WHITE
# #                 ctrl.border = ft.border.all(1, self.color_borde)
# #                 ctrl.scale = ft.Scale(1.0)
                
# #                 # Obtener el contenido del botón
# #                 contenido = ctrl.content
                
# #                 # Si es el botón de Alertas (con Stack)
# #                 if index == 2 and isinstance(contenido, ft.Stack):
# #                     boton_container = contenido.controls[0]
# #                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
# #                         row_controls = boton_container.content.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_texto_secundario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_texto
# #                 else:
# #                     # Para botones normales
# #                     if isinstance(contenido, ft.Row):
# #                         row_controls = contenido.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_texto_secundario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_texto
        
# #         # Usar try-except para evitar errores si la página no está lista
# #         try:
# #             ctrl.update()
# #         except:
# #             pass

# #     def inicializar_alertas_view(self):
# #         """Inicializa AlertasView después de que todo esté listo"""
# #         self.alertas_view = AlertasView(self.sistema_alertas, self.page)
# #         self.actualizar_alertas_container()
        
# #         # Inicializar el contador de alertas DESPUÉS de que la página esté lista
# #         self.page.run_thread(self.inicializar_contador_alertas)

# #     def inicializar_contador_alertas(self):
# #         """Inicializa el contador de alertas después de que la página esté lista"""
# #         time.sleep(0.5)
# #         self.actualizar_contador_alertas()

# #     def actualizar_alertas_container(self):
# #         """Actualiza el contenedor de ALERTAS con el AlertasView"""
# #         if self.alertas_view is None:
# #             return
            
# #         self.calendar_container_1.content = ft.Column(
# #             expand=True,
# #             controls=[
# #                 ft.Container(
# #                     padding=10,
# #                     bgcolor=ft.Colors.WHITE,
# #                     border_radius=10,
# #                     shadow=ft.BoxShadow(
# #                         spread_radius=1,
# #                         blur_radius=5,
# #                         color=ft.Colors.GREY_300,
# #                     ),
# #                     content=ft.Row(
# #                         alignment=ft.MainAxisAlignment.CENTER,
# #                         controls=[
# #                             ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, color=ft.Colors.RED_700, size=28),
# #                             ft.Text(
# #                                 "Historial de Alertas del Sistema",
# #                                 size=20,
# #                                 weight=ft.FontWeight.BOLD,
# #                                 color=ft.Colors.BLUE_900
# #                             ),
# #                         ],
# #                         spacing=15
# #                     )
# #                 ),
# #                 ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
# #                 ft.Container(
# #                     expand=True,
# #                     bgcolor=ft.Colors.WHITE,
# #                     border_radius=15,
# #                     padding=10,
# #                     shadow=ft.BoxShadow(
# #                         spread_radius=1,
# #                         blur_radius=5,
# #                         color=ft.Colors.GREY_300,
# #                     ),
# #                     content=self.alertas_view
# #                 )
# #             ]
# #         )

# #     def actualizar_contador_alertas(self):
# #         """Actualiza el contador de alertas en el badge"""
# #         if self.notificacion_badge is not None:
# #             total_alertas = self.sistema_alertas.contar_alertas()
            
# #             # NO mostrar el badge si estamos en la página de Alertas
# #             if total_alertas > 0 and not self.en_pagina_alertas:
# #                 self.notificacion_badge.visible = True
# #                 self.notificacion_badge.content.value = str(total_alertas) if total_alertas <= 99 else "99+"
                
# #                 # Si hay muchas alertas, hacer el badge más pequeño
# #                 if total_alertas > 9:
# #                     self.notificacion_badge.width = 24
# #                     self.notificacion_badge.height = 20
# #                 else:
# #                     self.notificacion_badge.width = 20
# #                     self.notificacion_badge.height = 20
# #             else:
# #                 self.notificacion_badge.visible = False
            
# #             # Actualizar el badge de forma segura
# #             try:
# #                 self.notificacion_badge.update()
# #             except Exception as e:
# #                 print(f"Error actualizando badge: {e}")

# #     def agregar_alerta_y_actualizar(self, causa, pagina):
# #         """Agrega una alerta y actualiza la vista y el contador"""
# #         # Agregar la alerta al sistema
# #         self.sistema_alertas.agregar_alerta(causa, pagina)
        
# #         # Actualizar el contador de notificaciones
# #         self.actualizar_contador_alertas()
        
# #         # Notificar a AlertasView si está en la página actual
# #         if self.alertas_view is not None and hasattr(self.alertas_view, 'en_pagina') and self.alertas_view.en_pagina:
# #             self.page.run_thread(self.alertas_view.cargar_ui)
# #             print(f"✓ Alerta agregada y vista actualizada: {causa}")

# #     def registrar_manual(self, e=None):
# #         """Registra un dato manualmente desde el botón en Home"""
# #         print("Registro manual solicitado")
# #         datos_actuales = self.obtener_datos_actuales_redondeados()
        
# #         registro = self.reloj_global.agregar_al_historial(
# #             datos_actuales, 
# #             tipo="registro_manual", 
# #             fuente="Manual (Home)"
# #         )
        
# #         self.agregar_alerta_y_actualizar(
# #             causa="Registro manual ejecutado desde Home",
# #             pagina="UMA"
# #         )
        
# #         self.mostrar_notificacion("✓ Registro manual agregado", ft.Colors.GREEN)
    
# #     def limpiar_historial_completamente(self, e=None):
# #         """Limpia todo el historial"""
# #         def confirmar_limpieza(e):
# #             self.reloj_global.limpiar_historial()
# #             dlg_modal.open = False
# #             self.page.update()
# #             self.mostrar_notificacion("✓ Historial limpiado", ft.Colors.GREEN)
            
# #             self.agregar_alerta_y_actualizar(
# #                 causa="Historial de registros limpiado",
# #                 pagina="UMA"
# #             )
        
# #         def cancelar_limpieza(e):
# #             dlg_modal.open = False
# #             self.page.update()
        
# #         dlg_modal = ft.AlertDialog(
# #             modal=True,
# #             title=ft.Text("Confirmar limpieza"),
# #             content=ft.Text("¿Está seguro que desea eliminar TODOS los registros del historial?\nEsta acción no se puede deshacer."),
# #             actions=[
# #                 ft.TextButton("Cancelar", on_click=cancelar_limpieza),
# #                 ft.ElevatedButton(
# #                     "Limpiar Todo", 
# #                     on_click=confirmar_limpieza,
# #                     bgcolor=ft.Colors.RED,
# #                     color=ft.Colors.WHITE
# #                 ),
# #             ],
# #             actions_alignment=ft.MainAxisAlignment.END,
# #         )
        
# #         self.page.dialog = dlg_modal
# #         dlg_modal.open = True
# #         self.page.update()
    
# #     def mostrar_notificacion(self, mensaje, color):
# #         """Muestra una notificación temporal"""
# #         snackbar = ft.SnackBar(
# #             content=ft.Text(mensaje, color=ft.Colors.WHITE),
# #             bgcolor=color,
# #             duration=2000,
# #         )
# #         self.page.snack_bar = snackbar
# #         snackbar.open = True
# #         self.page.update()

# #     def mostrar_banner_inicio(self):
# #         self.banner.open = True
# #         self.page.update()

# #     def cerrar_banner(self, e):
# #         self.banner.open = False
# #         self.page.update()

# #     def _on_alarma(self, hora):
# #         """Se ejecuta cuando el reloj global detecta una alarma"""
# #         print(f"UI: Alarma recibida: {hora}")
        
# #         datos_actuales = self.obtener_datos_actuales_redondeados()
        
# #         if hasattr(self, 'excel_manager'):
# #             self.excel_manager.guardar_todos(datos_actuales)
            
# #         registro = self.reloj_global.agregar_al_historial(
# #             datos_actuales, 
# #             tipo="registro_automatico", 
# #             fuente=f"Alarma {hora}"
# #         )
        
# #         self.agregar_alerta_y_actualizar(
# #             causa=f"Registro automático ejecutado a las {hora}",
# #             pagina="Reloj Global"
# #         )
        
# #         # FORZAR ACTUALIZACIÓN DE UMA INMEDIATAMENTE
# #         if hasattr(self, 'uma_instance'):
# #             self.page.run_thread(lambda: self.uma_instance.actualizar_lista())
        
# #         # Si estamos en la página de gráficas, actualizar
# #         if self.container_1.content == self.grafica_container and self.manometro_numero is not None:
# #             self.page.run_thread(self.actualizar_historial_manometro)
        
# #         self.mostrar_notificacion(f"✓ Registro automático a las {hora}", ft.Colors.BLUE)

# #     def obtener_datos_actuales_redondeados(self):
# #         """Obtiene los datos actuales redondeados"""
# #         datos = self.datos_tiempo_real.copy()
# #         datos['temperatura'] = round(datos['temperatura'], 1)
# #         datos['humedad'] = round(datos['humedad'])
# #         datos['presion1'] = round(datos['presion1'], 1)
# #         datos['presion2'] = round(datos['presion2'], 1)
# #         datos['presion3'] = round(datos['presion3'], 1)
# #         return datos

# #     def _initialize_ui_components(self):
# #         """Inicializa todos los componentes de la interfaz de usuario"""

# #         # 1. Crear controles de texto para UMA
# #         self.txt_temp_home = ft.Text("-- °C", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
# #         self.txt_hum_home = ft.Text("-- %", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
# #         self.txt_pres_home = ft.Text("-- Pa", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
        
# #         # 2. Crear UMA
# #         self.uma_instance = UMA(
# #             txt_temp=self.txt_temp_home,
# #             txt_hum=self.txt_hum_home,
# #             txt_pres=self.txt_pres_home,
# #             page=self.page,
# #             reloj_global=self.reloj_global
# #         )

# #         # 3. Crear manómetros CON CALLBACKS
# #         self.blue_box_presion1 = BlueBox(
# #             texto_titulo="MANOMETRO 1",
# #             texto=f"{self.datos_tiempo_real['presion1']} Pa", 
# #             mostrar_boton=False,
# #             on_grafica_click=self.abrir_pagina_grafica
# #         )
        
# #         self.blue_box_presion2 = BlueBox(
# #             texto_titulo="MANOMETRO 2",
# #             texto=f"{self.datos_tiempo_real['presion2']} Pa", 
# #             mostrar_boton=False,
# #             on_grafica_click=self.abrir_pagina_grafica
# #         )
        
# #         self.blue_box_presion3 = BlueBox(
# #             texto_titulo="MANOMETRO 3",
# #             texto=f"{self.datos_tiempo_real['presion3']} Pa", 
# #             mostrar_boton=False,
# #             on_grafica_click=self.abrir_pagina_grafica
# #         )
        
# #         self.blue_boxes = {
# #             'presion1': self.blue_box_presion1,
# #             'presion2': self.blue_box_presion2,
# #             'presion3': self.blue_box_presion3,
# #         }

# #         self.config_container = ConfiguracionContainer(self.page, self.reloj_global)

# #         ################################### PAGINA 1 (UMA) ####################################
# #         self.home_container_1 = ft.Container(
# #             bgcolor=self.color_teal,
# #             border_radius=20,
# #             expand=True,
# #             padding=20,
# #             alignment=ft.alignment.center,
# #             content=ft.Column(
# #                 expand=True,
# #                 controls=[
# #                     self.uma_instance,
# #                 ]
# #             )
# #         )

# #         ################################### PAGINA 2 (MANOMETROS) ####################################
# #         self.location_container_1 = ft.Container(
# #             bgcolor=self.color_teal,
# #             border_radius=20,
# #             expand=True,
# #             padding=20,
# #             content=ft.Column(
# #                 alignment=ft.MainAxisAlignment.START,
# #                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                 expand=True,
# #                 controls=[
# #                     ft.Container(
# #                         expand=True,
# #                         bgcolor=ft.Colors.WHITE,
# #                         border_radius=20,
# #                         alignment=ft.alignment.center,
# #                         padding=20,
# #                         shadow=ft.BoxShadow(
# #                             spread_radius=1,
# #                             blur_radius=10,
# #                             color=ft.Colors.GREY_300,
# #                         ),
# #                         content=ft.Column(
# #                             scroll=ft.ScrollMode.AUTO,
# #                             spacing=30,
# #                             controls=[
# #                                 ft.Row(
# #                                     alignment=ft.MainAxisAlignment.CENTER,
# #                                     vertical_alignment=ft.CrossAxisAlignment.CENTER,
# #                                     spacing=30,
# #                                     controls=[
# #                                         self.blue_box_presion1,
# #                                         self.blue_box_presion2,
# #                                         self.blue_box_presion3,
# #                                     ]
# #                                 )
# #                             ]
# #                         )
# #                     )
# #                 ]
# #             )
# #         )

# #         ################################### PAGINA 3 (ALERTAS) ####################################
# #         self.calendar_container_1 = ft.Container(
# #             bgcolor=self.color_teal,
# #             border_radius=20,
# #             expand=True,
# #             padding=20,
# #             content=ft.Container()
# #         )

# #         ################################### PAGINA 4 (CONFIGURACION) ####################################
# #         self.setting_container_1 = ft.Container(
# #             bgcolor=self.color_teal,
# #             border_radius=20,
# #             expand=True,
# #             padding=20,
# #             content=ft.Column(
# #                 alignment=ft.MainAxisAlignment.CENTER,
# #                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                 expand=True,
# #                 controls=[self.config_container]
# #             )
# #         )

# #         ################################### PÁGINA 5 (GRÁFICAS) ####################################
# #         # Los textos que se actualizarán dinámicamente
# #         self.titulo_grafica_text = ft.Text(
# #             value="Gráfica del Manómetro",
# #             size=24,
# #             weight=ft.FontWeight.BOLD,
# #             color=ft.Colors.BLUE_900
# #         )
        
# #         # ¡IMPORTANTE! Este Text mostrará el valor ACTUAL en tiempo real
# #         self.presion_actual_display = ft.Text(
# #             value="-- Pa",  # Valor inicial
# #             size=20,
# #             weight=ft.FontWeight.BOLD,
# #             color=ft.Colors.GREEN_700
# #         )
        
# #         # Gráfica
# #         self.grafica_chart = ft.LineChart(
# #             expand=True,
# #             tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
# #             border=ft.border.all(1, ft.Colors.GREY_300),
# #             horizontal_grid_lines=ft.ChartGridLines(
# #                 interval=1, color=ft.Colors.GREY_300, width=1
# #             ),
# #             vertical_grid_lines=ft.ChartGridLines(
# #                 interval=1, color=ft.Colors.GREY_300, width=1
# #             ),
# #             left_axis=ft.ChartAxis(
# #                 labels_size=40,
# #                 title=ft.Text("Presión (Pa)", size=12)
# #             ),
# #             bottom_axis=ft.ChartAxis(
# #                 labels_size=40,
# #                 title=ft.Text("Registros", size=12)
# #             ),
# #             min_y=80,
# #             max_y=110,
# #         )
        
# #         # Línea de la gráfica
# #         self.linea_grafica = ft.LineChartData(
# #             color=ft.Colors.BLUE_700,
# #             stroke_width=2,
# #             curved=True,
# #             stroke_cap_round=True,
# #             below_line_gradient=ft.LinearGradient(
# #                 begin=ft.alignment.top_center,
# #                 end=ft.alignment.bottom_center,
# #                 colors=[
# #                     ft.Colors.with_opacity(0.25, ft.Colors.BLUE),
# #                     "transparent",
# #                 ],
# #             ),
# #         )
        
# #         # Lista de historial para gráficas
# #         self.lista_historial_grafica = ft.ListView(
# #             expand=True,
# #             spacing=5,
# #             padding=10
# #         )
        
# #         # Contador de registros
# #         self.contador_registros = ft.Text(
# #             "0 registros",
# #             size=14,
# #             color=ft.Colors.GREY_600
# #         )
        
# #         # Botón de actualizar
# #         self.btn_actualizar_grafica = ft.IconButton(
# #             icon=ft.Icons.REFRESH,
# #             icon_color=ft.Colors.BLUE_600,
# #             tooltip="Actualizar gráfica",
# #             on_click=lambda e: self.actualizar_historial_manometro()
# #         )
        
# #         self.grafica_container = ft.Container(
# #             bgcolor=self.color_teal,
# #             border_radius=20,
# #             expand=True,
# #             padding=20,
# #             content=ft.Column(
# #                 expand=True,
# #                 spacing=20,
# #                 controls=[
# #                     # CABECERA
# #                     ft.Container(
# #                         padding=ft.padding.symmetric(vertical=10, horizontal=15),
# #                         bgcolor=ft.Colors.WHITE,
# #                         border_radius=10,
# #                         shadow=ft.BoxShadow(
# #                             spread_radius=1,
# #                             blur_radius=5,
# #                             color=ft.Colors.GREY_300,
# #                         ),
# #                         content=ft.Row(
# #                             alignment=ft.MainAxisAlignment.START,
# #                             vertical_alignment=ft.CrossAxisAlignment.CENTER,
# #                             spacing=20,
# #                             controls=[
# #                                 ft.IconButton(
# #                                     icon=ft.Icons.ARROW_BACK,
# #                                     icon_color=ft.Colors.BLUE_700,
# #                                     icon_size=28,
# #                                     on_click=lambda e: self.change_page_manual(1),
# #                                     tooltip="Volver a Manómetros"
# #                                 ),
# #                                 self.titulo_grafica_text,
# #                                 self.btn_actualizar_grafica
# #                             ]
# #                         )
# #                     ),
                    
# #                     # CONTENIDO PRINCIPAL
# #                     ft.Container(
# #                         expand=True,
# #                         bgcolor=ft.Colors.WHITE,
# #                         border_radius=15,
# #                         padding=25,
# #                         shadow=ft.BoxShadow(
# #                             spread_radius=1,
# #                             blur_radius=10,
# #                             color=ft.Colors.GREY_300,
# #                         ),
# #                         content=ft.Row(
# #                             expand=True,
# #                             spacing=20,
# #                             controls=[
# #                                 # Panel izquierdo - Grafica
# #                                 ft.Container(
# #                                     expand=2,  # 2/3 del espacio
# #                                     padding=20,
# #                                     bgcolor=ft.Colors.WHITE,
# #                                     border_radius=10,
# #                                     content=ft.Column(
# #                                         expand=True,
# #                                         spacing=10,
# #                                         controls=[
# #                                             ft.Row(
# #                                                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                                                 controls=[
# #                                                     ft.Text("Gráfica de Presión", 
# #                                                         size=18, weight=ft.FontWeight.BOLD),
# #                                                     self.contador_registros
# #                                                 ]
# #                                             ),
                                            
# #                                             ft.Divider(height=1, color=ft.Colors.GREY_300),
                                            
# #                                             # Gráfica
# #                                             ft.Container(
# #                                                 expand=True,
# #                                                 border=ft.border.all(1, ft.Colors.GREY_300),
# #                                                 border_radius=10,
# #                                                 padding=10,
# #                                                 content=self.grafica_chart
# #                                             ),
                                            
# #                                             # Info adicional
# #                                             ft.Container(
# #                                                 padding=10,
# #                                                 bgcolor=ft.Colors.BLUE_50,
# #                                                 border_radius=5,
# #                                                 content=ft.Row(
# #                                                     spacing=10,
# #                                                     controls=[
# #                                                         ft.Text("Presión actual:", size=14, color=ft.Colors.GREY_600),
# #                                                         self.presion_actual_display,
# #                                                     ]
# #                                                 )
# #                                             )
# #                                         ]
# #                                     )
# #                                 ),
# #                                 # Panel derecho - Historial
# #                                 ft.Container(
# #                                     expand=1,  # 1/3 del espacio
# #                                     padding=20,
# #                                     bgcolor=ft.Colors.WHITE,
# #                                     border_radius=10,
# #                                     content=ft.Column(
# #                                         expand=True,
# #                                         spacing=10,
# #                                         controls=[
# #                                             ft.Row(
# #                                                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                                                 controls=[
# #                                                     ft.Text("Historial de Registros", 
# #                                                         size=18, weight=ft.FontWeight.BOLD),
# #                                                 ]
# #                                             ),
# #                                             # ENCABEZADO DE TABLA
# #                                             ft.Container(
# #                                                 padding=10,
# #                                                 bgcolor=ft.Colors.BLUE_100,
# #                                                 border_radius=5,
# #                                                 margin=ft.margin.only(bottom=5),
# #                                                 content=ft.Row([
# #                                                     ft.Container(
# #                                                         width=80,
# #                                                         content=ft.Text("Presión", 
# #                                                                     weight=ft.FontWeight.BOLD,
# #                                                                     color=ft.Colors.BLUE_800,
# #                                                                     size=12)
# #                                                     ),
# #                                                     ft.Container(
# #                                                         width=80,
# #                                                         content=ft.Text("Fecha", 
# #                                                                     weight=ft.FontWeight.BOLD,
# #                                                                     color=ft.Colors.BLUE_800,
# #                                                                     size=12)
# #                                                     ),
# #                                                     ft.Container(
# #                                                         width=60,
# #                                                         content=ft.Text("Hora", 
# #                                                                     weight=ft.FontWeight.BOLD,
# #                                                                     color=ft.Colors.BLUE_800,
# #                                                                     size=12)
# #                                                     ),
# #                                                     ft.Container(
# #                                                         width=60,
# #                                                         content=ft.Text("Tipo", 
# #                                                                     weight=ft.FontWeight.BOLD,
# #                                                                     color=ft.Colors.BLUE_800,
# #                                                                     size=12)
# #                                                     ),
# #                                                 ])
# #                                             ),
                                            
# #                                             ft.Divider(height=1, color=ft.Colors.GREY_300),
                                            
# #                                             # Área de historial
# #                                             ft.Container(
# #                                                 expand=True,
# #                                                 border=ft.border.all(1, ft.Colors.GREY_300),
# #                                                 border_radius=10,
# #                                                 padding=10,
# #                                                 content=self.lista_historial_grafica
# #                                             ),
                                            
# #                                             # Leyenda
# #                                             ft.Container(
# #                                                 padding=10,
# #                                                 content=ft.Row(
# #                                                     spacing=15,
# #                                                     alignment=ft.MainAxisAlignment.CENTER,
# #                                                     controls=[
# #                                                         ft.Row([
# #                                                             ft.Container(width=12, height=12, 
# #                                                                     bgcolor=ft.Colors.BLUE_50, 
# #                                                                     border_radius=6),
# #                                                             ft.Text("Automático", size=10),
# #                                                         ]),
# #                                                         ft.Row([
# #                                                             ft.Container(width=12, height=12, 
# #                                                                     bgcolor=ft.Colors.GREEN_50, 
# #                                                                     border_radius=6),
# #                                                             ft.Text("Manual", size=10),
# #                                                         ]),
# #                                                     ]
# #                                                 )
# #                                             )
# #                                         ]
# #                                     )
# #                                 )
# #                             ]
# #                         )
# #                     )
# #                 ]
# #             )
# #         )

# #         # NUEVO: Agregar la página de gráficas a la lista
# #         self.container_list_1 = [
# #             self.home_container_1,      # índice 0: UMA
# #             self.location_container_1,  # índice 1: Manómetros  
# #             self.calendar_container_1,  # índice 2: Alertas
# #             self.setting_container_1,   # índice 3: Configuración
# #             self.grafica_container      # NUEVO índice 4: Gráficas
# #         ]

# #         self.container_1 = ft.Container(
# #             content=self.container_list_1[0], 
# #             expand=True,
# #             animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
# #         )

# #         # ========== BARRA DE NAVEGACIÓN PROFESIONAL ==========
# #         # Botones de navegación con diseño profesional
# #         self.btn_connect = self._crear_boton_navegacion_profesional("UMA", ft.Icons.MONITOR_HEART, 0)
# #         self.btn_connect2 = self._crear_boton_navegacion_profesional("Manómetros", ft.Icons.SPEED, 1)
# #         self.btn_connect3 = self._crear_boton_navegacion_profesional("Alertas", ft.Icons.NOTIFICATIONS, 2)
# #         self.btn_connect4 = self._crear_boton_navegacion_profesional("Configuración", ft.Icons.SETTINGS, 3)

# #         # Barra lateral de navegación profesional
# #         self.navigation_container = ft.Container(
# #             col=2,
# #             expand=True,
# #             bgcolor=ft.Colors.WHITE,
# #             border_radius=0,
# #             border=ft.border.only(right=ft.border.BorderSide(1, self.color_borde)),
# #             padding=ft.padding.symmetric(vertical=30, horizontal=20),
# #             shadow=ft.BoxShadow(
# #                 spread_radius=0,
# #                 blur_radius=20,
# #                 color="rgba(39, 245, 180, 0.08)",
# #                 offset=ft.Offset(5, 0)
# #             ),
# #             content=ft.Column(
# #                 alignment=ft.MainAxisAlignment.START,
# #                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                 expand=True,
# #                 spacing=15,
# #                 controls=[
# #                     # Logo y nombre
# #                     ft.Container(
# #                         padding=ft.padding.only(bottom=30),
# #                         content=ft.Column(
# #                             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                             spacing=10,
# #                             controls=[
# #                                 ft.Container(
# #                                     width=60,
# #                                     height=60,
# #                                     border_radius=15,
# #                                     bgcolor=self.color_primario,
# #                                     alignment=ft.alignment.center,
# #                                     shadow=ft.BoxShadow(
# #                                         spread_radius=0,
# #                                         blur_radius=15,
# #                                         color="rgba(39, 245, 180, 0.15)",
# #                                     ),
# #                                     content=ft.Icon(
# #                                         ft.Icons.MONITOR_HEART,
# #                                         color=ft.Colors.WHITE,
# #                                         size=30
# #                                     )
# #                                 ),
# #                                 ft.Column(
# #                                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                                     spacing=2,
# #                                     controls=[
# #                                         ft.Text(
# #                                             "Sistema de",
# #                                             size=14,
# #                                             weight=ft.FontWeight.BOLD,
# #                                             color=self.color_texto
# #                                         ),
# #                                         ft.Text(
# #                                             "Monitoreo",
# #                                             size=14,
# #                                             weight=ft.FontWeight.BOLD,
# #                                             color=self.color_primario
# #                                         )
# #                                     ]
# #                                 )
# #                             ]
# #                         )
# #                     ),
                    
# #                     ft.Divider(height=20, color=self.color_borde),
                    
# #                     # Botones de navegación
# #                     self.btn_connect,
# #                     self.btn_connect2,
# #                     self.btn_connect3,
# #                     self.btn_connect4,
                    
# #                     ft.Divider(height=30, color=self.color_borde),
                    
# #                     # Estado del sistema
# #                     ft.Container(
# #                         padding=15,
# #                         bgcolor=f"{self.color_primario}08",
# #                         border_radius=10,
# #                         content=ft.Column(
# #                             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                             spacing=8,
# #                             controls=[
# #                                 ft.Row(
# #                                     spacing=8,
# #                                     controls=[
# #                                         ft.Container(
# #                                             width=10,
# #                                             height=10,
# #                                             border_radius=5,
# #                                             bgcolor=self.color_primario
# #                                         ),
# #                                         ft.Text(
# #                                             "Sistema Activo",
# #                                             size=12,
# #                                             weight=ft.FontWeight.W_600,
# #                                             color=self.color_texto
# #                                         )
# #                                     ]
# #                                 ),
# #                                 ft.Text(
# #                                     datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
# #                                     size=11,
# #                                     color=self.color_texto_secundario
# #                                 )
# #                             ]
# #                         )
# #                     )
# #                 ]
# #             )
# #         )

# #         # Área principal de contenido
# #         self.frame_2 = ft.Container(
# #             col=10,
# #             alignment=ft.alignment.center,
# #             bgcolor=self.color_teal,
# #             expand=True,
# #             content=ft.Column(
# #                 expand=True,
# #                 controls=[
# #                     self.container_1,
# #                 ]
# #             )   
# #         )
        
# #         # Layout principal
# #         self.resp_container = ft.ResponsiveRow(
# #             vertical_alignment=ft.CrossAxisAlignment.STRETCH,
# #             controls=[
# #                 self.navigation_container,
# #                 self.frame_2,
# #             ]
# #         )

# #         self.iniciar_home_random()
        
# #         # Inicializar botón activo
# #         self.actualizar_colores_botones(0)

# #     def redondear_entero_desde_6(self, valor):
# #         """Redondea hacia arriba desde 0.6"""
# #         parte_entera = int(valor)
# #         decimal = valor - parte_entera
# #         return parte_entera + 1 if decimal >= 0.6 else parte_entera
    
# #     def generar_datos_random(self):
# #         """Genera datos aleatorios con verificación de alertas"""
# #         temp_original = random.uniform(15, 35)
# #         hum_original = random.uniform(30, 90)
# #         pres1_original = random.uniform(80, 110)
# #         pres2_original = random.uniform(80, 110)
# #         pres3_original = random.uniform(80, 110)

# #         temp = self.redondear_entero_desde_6(temp_original)
# #         hum = self.redondear_entero_desde_6(hum_original)
# #         pres1 = self.redondear_entero_desde_6(pres1_original)
# #         pres2 = self.redondear_entero_desde_6(pres2_original)
# #         pres3 = self.redondear_entero_desde_6(pres3_original)

# #         self.datos_tiempo_real = {
# #             'temperatura': temp,
# #             'humedad': hum, 
# #             'presion1': pres1,
# #             'presion2': pres2,
# #             'presion3': pres3,
# #         }

# #         # Actualizar manómetros
# #         for key, box in self.blue_boxes.items():
# #             if hasattr(box, 'actualizar_valor'):
# #                 valor = self.datos_tiempo_real[key]
# #                 box.actualizar_valor(f"{valor} Pa")

# #         # Verificar alertas - usar el nuevo método
# #         if temp > 30:
# #             self.agregar_alerta_y_actualizar(
# #                 causa=f"Temperatura CRÍTICA: {temp}°C (supera 30°C)",
# #                 pagina="UMA"
# #             )
        
# #         if hum > 85:
# #             self.agregar_alerta_y_actualizar(
# #                 causa=f"Humedad ALTA: {hum}% (superior a 85%)",
# #                 pagina="UMA"
# #             )
        
# #         if pres1 > 108:
# #             self.agregar_alerta_y_actualizar(
# #                 causa=f"Presión ALTA: {pres1}Pa (supera 108 Pa)",
# #                 pagina="UMA"
# #             )
        
# #         if pres2 > 108:
# #             self.agregar_alerta_y_actualizar(
# #                 causa=f"Presión ALTA: {pres2}Pa (supera 108 Pa)",
# #                 pagina="UMA"
# #             )
        
# #         if pres3 > 108:
# #             self.agregar_alerta_y_actualizar(
# #                 causa=f"Presión ALTA: {pres3}Pa (supera 108 Pa)",
# #                 pagina="UMA"
# #             )
        
# #         return {"presion1": pres1, "presion2": pres2, "presion3": pres3, "temperatura": temp, "humedad": hum}

# #     def iniciar_home_random(self):
# #         """Inicia la generación aleatoria de datos"""
# #         def loop():
# #             while True:
# #                 datos = self.generar_datos_random()
                
# #                 def actualizar():
# #                     # Actualiza los controles que UMA usa
# #                     self.txt_temp_home.value = f"{datos['temperatura']} °C"
# #                     self.txt_hum_home.value = f"{datos['humedad']} %"
# #                     self.txt_pres_home.value = f"{datos['presion1']} Pa"
                    
# #                     # ¡NUEVO! Actualizar también la página de gráficas si estamos en ella
# #                     if (hasattr(self, 'manometro_activo') and 
# #                         hasattr(self, 'presion_actual_display') and
# #                         self.container_1.content == self.grafica_container):
                        
# #                         # Obtener el valor directamente como dijiste
# #                         if "MANOMETRO 1" in self.manometro_activo:
# #                             self.presion_actual_display.value = f"{self.datos_tiempo_real['presion1']} Pa"
# #                         elif "MANOMETRO 2" in self.manometro_activo:
# #                             self.presion_actual_display.value = f"{self.datos_tiempo_real['presion2']} Pa"
# #                         elif "MANOMETRO 3" in self.manometro_activo:
# #                             self.presion_actual_display.value = f"{self.datos_tiempo_real['presion3']} Pa"
                    
# #                     self.page.update()
                
# #                 self.page.run_thread(actualizar)
# #                 time.sleep(2)  # Ya tienes este intervalo
        
# #         threading.Thread(target=loop, daemon=True).start()

# #     def change_page_manual(self, index):
# #         """Cambia entre páginas de la aplicación"""
# #         self.container_1.content = self.container_list_1[index]
# #         self.actualizar_colores_botones(index)
        
# #         # Actualizar estado de la página de Alertas
# #         if index == 2:  # Si estamos entrando a Alertas
# #             self.en_pagina_alertas = True
# #             # Ocultar el badge
# #             if self.notificacion_badge is not None:
# #                 self.notificacion_badge.visible = False
# #                 try:
# #                     self.notificacion_badge.update()
# #                 except:
# #                     pass
# #         else:  # Si estamos saliendo de Alertas
# #             self.en_pagina_alertas = False
# #             # Actualizar el contador para que se muestre si hay alertas
# #             self.actualizar_contador_alertas()
        
# #         # Si estamos entrando a la página de gráficas, actualizar datos
# #         if index == 4 and self.manometro_activo and self.manometro_numero:
# #             self.page.run_thread(self.actualizar_historial_manometro)
        
# #         if self.alertas_view is not None:
# #             if index == 2:  # Alertas está en índice 2
# #                 if hasattr(self.alertas_view, 'entrar_a_pagina'):
# #                     self.alertas_view.entrar_a_pagina()
# #             else:
# #                 if hasattr(self.alertas_view, 'salir_de_pagina'):
# #                     self.alertas_view.salir_de_pagina()

# #         self.page.update()
    
# #     def actualizar_colores_botones(self, index_activo):
# #         """Actualiza los colores y formas de los botones de navegación"""
# #         botones = [self.btn_connect, self.btn_connect2, self.btn_connect3, self.btn_connect4]
        
# #         for i, btn in enumerate(botones):
# #             if i == index_activo:
# #                 # Botón activo: Color primario con fondo
# #                 btn.bgcolor = self.color_primario
# #                 btn.border = ft.border.all(1, self.color_primario)
                
# #                 # Obtener el contenido del botón
# #                 contenido = btn.content
                
# #                 # Si es el botón de Alertas (con Stack)
# #                 if i == 2 and isinstance(contenido, ft.Stack):
# #                     boton_container = contenido.controls[0]
# #                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
# #                         row_controls = boton_container.content.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = ft.Colors.WHITE
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = ft.Colors.WHITE
# #                 else:
# #                     # Para botones normales
# #                     if isinstance(contenido, ft.Row):
# #                         row_controls = contenido.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = ft.Colors.WHITE
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = ft.Colors.WHITE
# #                 btn.scale = ft.Scale(1.0)
# #             else:
# #                 # Botones inactivos: Blanco con borde gris
# #                 btn.bgcolor = ft.Colors.WHITE
# #                 btn.border = ft.border.all(1, self.color_borde)
                
# #                 # Obtener el contenido del botón
# #                 contenido = btn.content
                
# #                 # Si es el botón de Alertas (con Stack)
# #                 if i == 2 and isinstance(contenido, ft.Stack):
# #                     boton_container = contenido.controls[0]
# #                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
# #                         row_controls = boton_container.content.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_texto_secundario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_texto
# #                 else:
# #                     # Para botones normales
# #                     if isinstance(contenido, ft.Row):
# #                         row_controls = contenido.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_texto_secundario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_texto
# #                 btn.scale = ft.Scale(1.0)
        
# #         # Actualizar todos los botones de forma segura
# #         for btn in botones:
# #             try:
# #                 btn.update()
# #             except:
# #                 pass

# #     def abrir_pagina_grafica(self, titulo_manometro):
# #         """Abre la página de gráficas para un manómetro específico"""
# #         print(f"Abriendo gráfica para: {titulo_manometro}")
        
# #         # 1. Guardar referencia al manómetro activo
# #         self.manometro_activo = titulo_manometro
        
# #         # 2. Obtener datos del manómetro específico
# #         if "MANOMETRO 1" in titulo_manometro:
# #             self.manometro_numero = 1
# #             datos = self.datos_tiempo_real['presion1']
# #         elif "MANOMETRO 2" in titulo_manometro:
# #             self.manometro_numero = 2
# #             datos = self.datos_tiempo_real['presion2']
# #         elif "MANOMETRO 3" in titulo_manometro:
# #             self.manometro_numero = 3
# #             datos = self.datos_tiempo_real['presion3']
# #         else:
# #             self.manometro_numero = None
# #             datos = 0
        
# #         # 3. Actualizar el título de la página
# #         self.titulo_grafica_text.value = f"Gráfica: {titulo_manometro}"
        
# #         # 4. Actualizar el valor inicial en el display
# #         self.presion_actual_display.value = f"{datos} Pa"
        
# #         # 5. Cambiar a la página de gráficas (índice 4)
# #         self.change_page_manual(4)
        
# #         # 6. Actualizar historial y gráfica
# #         self.page.run_thread(self.actualizar_historial_manometro)
        
# #         # 7. Imprimir confirmación
# #         print(f"✓ Página de gráficas abierta para {titulo_manometro}")
# #         print(f"  Presión actual: {datos} Pa")
# #         print(f"  Número de manómetro: {self.manometro_numero}")

# #     def crear_punto_grafica(self, x, y):
# #         """Crea un punto de datos para la gráfica"""
# #         return ft.LineChartDataPoint(
# #             x,
# #             y,
# #             selected_below_line=ft.ChartPointLine(
# #                 width=0.5, color=ft.Colors.GREY_400, dash_pattern=[2, 4]
# #             ),
# #             selected_point=ft.ChartCirclePoint(
# #                 stroke_width=2, 
# #                 color=ft.Colors.BLUE_700,
# #                 radius=4
# #             ),
# #         )

# #     def actualizar_historial_manometro(self, e=None):
# #         """Actualiza la gráfica y la lista de historial para el manómetro activo"""
# #         if not self.manometro_activo or not self.manometro_numero:
# #             print("No hay manómetro activo")
# #             return
        
# #         print(f"Actualizando historial para manómetro {self.manometro_numero}")
        
# #         # Obtener registros del manómetro desde el historial principal
# #         registros = self.reloj_global.obtener_registros_por_manometro(
# #             self.manometro_numero, 
# #             limite=30
# #         )
        
# #         # Actualizar contador
# #         self.contador_registros.value = f"{len(registros)} registros"
        
# #         # Limpiar gráfica actual
# #         puntos_grafica = []
# #         self.grafica_chart.data_series = []
        
# #         # Agregar puntos a la gráfica (X = índice, Y = presión)
# #         for i, registro in enumerate(registros):
# #             punto = self.crear_punto_grafica(i, registro['presion'])
# #             puntos_grafica.append(punto)
        
# #         # Actualizar línea de la gráfica
# #         self.linea_grafica.data_points = puntos_grafica
# #         self.grafica_chart.data_series = [self.linea_grafica]
        
# #         # Limpiar lista actual
# #         self.lista_historial_grafica.controls.clear()
        
# #         # Agregar registros a la lista (más reciente primero)
# #         for registro in registros:
# #             # Determinar color según tipo
# #             if "automatico" in registro['tipo']:
# #                 color_fondo = ft.Colors.BLUE_50
# #                 icono = ft.Icons.AUTORENEW
# #                 color_icono = ft.Colors.BLUE_600
# #             elif "manual" in registro['tipo']:
# #                 color_fondo = ft.Colors.GREEN_50
# #                 icono = ft.Icons.TOUCH_APP
# #                 color_icono = ft.Colors.GREEN_600
# #             else:
# #                 color_fondo = ft.Colors.GREY_50
# #                 icono = ft.Icons.INFO
# #                 color_icono = ft.Colors.GREY_600
            
# #             # Crear fila para la tabla
# #             fila = ft.Container(
# #                 padding=10,
# #                 bgcolor=ft.Colors.RED_50 if registro['presion'] > 108 else color_fondo,
# #                 border_radius=5,
# #                 margin=ft.margin.only(bottom=5),
# #                 content=ft.Row([
# #                     # Presión
# #                     ft.Container(
# #                         width=80,
# #                         content=ft.Text(
# #                             f"{registro['presion']} Pa",
# #                             size=12,
# #                             color=ft.Colors.RED_700 if registro['presion'] > 108 else ft.Colors.BLUE_700,
# #                             weight=ft.FontWeight.BOLD if registro['presion'] > 108 else ft.FontWeight.NORMAL
# #                         )
# #                     ),
# #                     # Fecha
# #                     ft.Container(
# #                         width=80,
# #                         content=ft.Text(
# #                             registro['fecha'],
# #                             size=12,
# #                             color=ft.Colors.GREY_700
# #                         )
# #                     ),
# #                     # Hora
# #                     ft.Container(
# #                         width=60,
# #                         content=ft.Text(
# #                             registro['hora'],
# #                             size=12,
# #                             color=ft.Colors.GREY_700
# #                         )
# #                     ),
# #                     # Tipo con icono
# #                     ft.Container(
# #                         width=60,
# #                         content=ft.Row([
# #                             ft.Icon(icono, size=14, color=color_icono),
# #                             ft.Text(
# #                                 "Auto" if "automatico" in registro['tipo'] else "Manual",
# #                                 size=10,
# #                                 color=color_icono
# #                             )
# #                         ], spacing=5)
# #                     ),
# #                 ])
# #             )
            
# #             self.lista_historial_grafica.controls.append(fila)
        
# #         # Si no hay registros, mostrar mensaje
# #         if not registros:
# #             self.lista_historial_grafica.controls.append(
# #                 ft.Container(
# #                     padding=20,
# #                     alignment=ft.alignment.center,
# #                     content=ft.Column(
# #                         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                         spacing=10,
# #                         controls=[
# #                             ft.Icon(ft.Icons.HISTORY, size=48, color=ft.Colors.GREY_400),
# #                             ft.Text(
# #                                 "No hay registros históricos",
# #                                 size=14,
# #                                 color=ft.Colors.GREY_500
# #                             )
# #                         ]
# #                     )
# #                 )
# #             )
        
# #         # Actualizar todos los componentes
# #         try:
# #             self.grafica_chart.update()
# #             self.lista_historial_grafica.update()
# #             self.contador_registros.update()
# #             self.presion_actual_display.update()
# #         except Exception as e:
# #             print(f"Error actualizando componentes: {e}")

# #     def will_unmount(self):
# #         """Detener el reloj global al cerrar la app"""
# #         self.reloj_global.detener()


# # def main(page: ft.Page):
# #     page.title = "Sistema de Monitoreo Inteligente"
# #     page.window.width = 1400
# #     page.window.height = 750
# #     page.window.resizable = True
# #     page.horizontal_alignment = "center"
# #     page.vertical_alignment = "center"
# #     page.theme_mode = ft.ThemeMode.LIGHT
# #     page.window.bgcolor = ft.Colors.WHITE
# #     page.padding = 0

# #     ui = UI(page)
# #     page.add(ui)

# # if __name__ == "__main__":
# #     ft.app(target=main)








































# # GRAFICA 2
# # import flet as ft
# # import threading
# # import time
# # import datetime
# # import json
# # import os
# # import random
# # from cajaAzul import BlueBox
# # from configuracion import ConfiguracionContainer
# # from excel5 import ExcelUnicoArchivo
# # from alertas import SistemaAlertas, AlertasView
# # from paguina1 import UMA

# # class RelojGlobal:
# #     def __init__(self):
# #         self.horas_registradas = []
# #         self.archivo_horas = "horas.json"
# #         self.historial_registros = []
# #         self.archivo_historial = "historial_registros.json"
# #         self.reloj_activo = True
# #         self.ultima_ejecucion = {}
# #         self.callbacks = []
# #         self.historial_callbacks = []
        
# #         # Cargar horas guardadas
# #         self.cargar_horas()
# #         self.cargar_historial()
# #         self.iniciar()

# #     def agregar_callback(self, callback):
# #         """Agrega una función que se ejecutará cuando suene una alarma"""
# #         self.callbacks.append(callback)
    
# #     def agregar_callback_historial(self, callback):
# #         """Agrega una función que se ejecutará cuando se agregue un nuevo registro al historial"""
# #         self.historial_callbacks.append(callback)

# #     def cargar_horas(self):
# #         """Carga las horas desde archivo JSON"""
# #         if os.path.exists(self.archivo_horas):
# #             try:
# #                 with open(self.archivo_horas, "r") as file:
# #                     datos = json.load(file)
# #                     self.horas_registradas = [
# #                         datetime.datetime.strptime(h, "%H:%M").time()
# #                         for h in datos
# #                     ]
# #                 print(f"RelojGlobal: Horas cargadas: {[h.strftime('%I:%M %p') for h in self.horas_registradas]}")
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error cargando horas: {e}")
# #                 self.horas_registradas = []
    
# #     def cargar_historial(self):
# #         """Carga el historial desde archivo JSON"""
# #         if os.path.exists(self.archivo_historial):
# #             try:
# #                 with open(self.archivo_historial, "r") as file:
# #                     self.historial_registros = json.load(file)
# #                 print(f"RelojGlobal: Historial cargado ({len(self.historial_registros)} registros)")
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error cargando historial: {e}")
# #                 self.historial_registros = []
# #         else:
# #             self.guardar_historial()

# #     def guardar_horas(self):
# #         """Guarda las horas en archivo JSON"""
# #         try:
# #             datos = [h.strftime("%H:%M") for h in self.horas_registradas]
# #             with open(self.archivo_horas, "w") as file:
# #                 json.dump(datos, file)
# #         except Exception as e:
# #             print(f"RelojGlobal: Error guardando horas: {e}")
    
# #     def guardar_historial(self):
# #         """Guarda el historial en archivo JSON"""
# #         try:
# #             if len(self.historial_registros) > 50:
# #                 self.historial_registros = self.historial_registros[-50:]
            
# #             with open(self.archivo_historial, "w") as file:
# #                 json.dump(self.historial_registros, file, indent=2)
# #         except Exception as e:
# #             print(f"RelojGlobal: Error guardando historial: {e}")

# #     def agregar_hora(self, hora_time):
# #         """Agrega una hora a la lista global"""
# #         if hora_time not in self.horas_registradas:
# #             self.horas_registradas.append(hora_time)
# #             self.guardar_horas()
# #             print(f"RelojGlobal: Hora agregada: {hora_time.strftime('%I:%M %p')}")
# #             return True
# #         return False

# #     def eliminar_hora(self, hora_time):
# #         """Elimina una hora de la lista global"""
# #         if hora_time in self.horas_registradas:
# #             self.horas_registradas.remove(hora_time)
# #             self.guardar_horas()
# #             print(f"RelojGlobal: Hora eliminada: {hora_time.strftime('%I:%M %p')}")
# #             return True
# #         return False
    
# #     def agregar_al_historial(self, datos, tipo="registro_automatico", fuente="Reloj Global"):
# #         """Agrega un registro al historial"""
# #         registro = {
# #             "fecha": datetime.datetime.now().strftime("%d/%m/%y"),
# #             "hora": datetime.datetime.now().strftime("%H:%M"),
# #             "datos": datos,
# #             "tipo": tipo,
# #             "fuente": fuente
# #         }
# #         self.historial_registros.append(registro)
# #         self.guardar_historial()
        
# #         # Notificar a todos los callbacks
# #         for callback in self.historial_callbacks:
# #             try:
# #                 callback()
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error en callback de historial: {e}")
        
# #         return registro
    
# #     def obtener_registros_por_manometro(self, manometro_numero, limite=20):
# #         """
# #         Obtiene todos los registros históricos para un manómetro específico.
# #         manometro_numero: 1, 2 o 3
# #         limite: cantidad máxima de registros a retornar
# #         """
# #         registros_manometro = []
        
# #         # Filtrar registros para este manómetro (más recientes primero)
# #         for registro in self.historial_registros[::-1]:  # Invertir para obtener más recientes primero
# #             if 'datos' in registro:
# #                 datos = registro['datos']
# #                 # Extraer la presión del manómetro específico
# #                 clave_presion = f'presion{manometro_numero}'
# #                 if clave_presion in datos:
# #                     # Convertir fecha y hora a datetime para ordenar
# #                     fecha_hora_str = f"{registro['fecha']} {registro['hora']}"
# #                     fecha_hora = datetime.datetime.strptime(fecha_hora_str, "%d/%m/%y %H:%M")
                    
# #                     registro_manometro = {
# #                         'fecha': registro['fecha'],
# #                         'hora': registro['hora'],
# #                         'fecha_hora': fecha_hora,
# #                         'presion': datos[clave_presion],
# #                         'tipo': registro.get('tipo', 'desconocido'),
# #                         'fuente': registro.get('fuente', 'desconocido')
# #                     }
# #                     registros_manometro.append(registro_manometro)
            
# #             # Limitar cantidad de registros
# #             if len(registros_manometro) >= limite:
# #                 break
        
# #         # Ordenar por fecha_hora (más antiguo primero para gráfica de izquierda a derecha)
# #         registros_manometro.sort(key=lambda x: x['fecha_hora'])
        
# #         return registros_manometro

# #     def limpiar_historial(self):
# #         """Limpia todo el historial"""
# #         self.historial_registros = []
# #         self.guardar_historial()
# #         print("RelojGlobal: Historial limpiado")
        
# #         # Notificar a los callbacks
# #         for callback in self.historial_callbacks:
# #             try:
# #                 callback()
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error en callback de limpieza: {e}")

# #     def iniciar(self):
# #         """Inicia el reloj global en un hilo separado"""
# #         if not hasattr(self, 'thread') or not self.thread.is_alive():
# #             self.thread = threading.Thread(target=self._loop, daemon=True)
# #             self.thread.start()
# #             print("RelojGlobal: Iniciado")

# #     def _loop(self):
# #         """Loop principal del reloj"""
# #         while self.reloj_activo:
# #             try:
# #                 ahora = datetime.datetime.now()
                
# #                 for hora_obj in self.horas_registradas:
# #                     hora_actual_minuto = ahora.strftime("%I:%M %p")
# #                     segundos = ahora.strftime("%S")
# #                     hora_objetivo_str = hora_obj.strftime("%I:%M %p")

# #                     if hora_actual_minuto == hora_objetivo_str and segundos == "00":
# #                         h_obj = datetime.datetime.combine(ahora.date(), hora_obj)
# #                         clave = h_obj.strftime("%Y-%m-%d %H:%M")

# #                         if clave not in self.ultima_ejecucion:
# #                             self.ultima_ejecucion[clave] = True
# #                             self._ejecutar_alarma(hora_objetivo_str)
# #                             print(f"RelojGlobal: ✓ Alarma: {hora_objetivo_str}")
                
# #                 hoy = datetime.datetime.now().date()
# #                 claves_a_eliminar = [k for k in self.ultima_ejecucion 
# #                                     if datetime.datetime.strptime(k.split(" ")[0], "%Y-%m-%d").date() < hoy]
# #                 for k in claves_a_eliminar:
# #                     del self.ultima_ejecucion[k]

# #                 time.sleep(1)
                
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error en loop: {e}")
# #                 time.sleep(1)

# #     def _ejecutar_alarma(self, hora):
# #         """Ejecuta todos los callbacks registrados"""
# #         for callback in self.callbacks:
# #             try:
# #                 callback(hora)
# #             except Exception as e:
# #                 print(f"RelojGlobal: Error en callback: {e}")

# #     def detener(self):
# #         """Detiene el reloj global"""
# #         self.reloj_activo = False


# # class UI(ft.Container):
# #     def __init__(self, page):
# #         super().__init__(expand=True)
# #         self.page = page
        
# #         # COLORES PARA LA BARRA DE NAVEGACIÓN
# #         self.color_primario = "#27F5B4"  # Verde agua
# #         self.color_fondo = "#FFFFFF"  # Blanco
# #         self.color_texto = "#2C3E50"  # Azul oscuro
# #         self.color_texto_secundario = "#6C757D"  # Gris
# #         self.color_borde = "#E9ECEF"  # Gris claro para bordes
        
# #         # Datos en tiempo real (manteniendo los originales)
# #         self.datos_tiempo_real = {
# #             'temperatura': 0,
# #             'humedad': 0, 
# #             'presion1': 0,
# #             'presion2': 0,
# #             'presion3': 0,
# #         }

# #         self.excel_manager = ExcelUnicoArchivo()
# #         self.bandera_excel = self.excel_manager.get_bandera_archivo()
        
# #         self.reloj_global = RelojGlobal()
# #         self.sistema_alertas = SistemaAlertas()
# #         self.alertas_view = None
        
# #         # Variable para el badge de notificaciones
# #         self.notificacion_badge = None
# #         # Variable para saber si estamos en la página de Alertas
# #         self.en_pagina_alertas = False
        
# #         # Variables para gráficas
# #         self.manometro_activo = None
# #         self.manometro_numero = None
# #         self.grafica_chart = None
# #         self.lista_historial_grafica = None
# #         self.titulo_grafica_text = None

# #         self.banner = ft.Banner(
# #             bgcolor=ft.Colors.AMBER_100,
# #             leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
# #             content=ft.Text(
# #                 "Sistema de monitoreo iniciado",
# #                 color=ft.Colors.BLACK,
# #             ),
# #             actions=[
# #                 ft.TextButton("OK", on_click=self.cerrar_banner)
# #             ],
# #         )
# #         self.page.controls.append(self.banner)

# #         if not self.bandera_excel:
# #             print("⚠️ Main: No se encontró archivo Excel, mostrando banner...")
# #             self.mostrar_banner_inicio()
# #         else:
# #             self.reloj_global.agregar_callback(self._on_alarma)
# #             print("✅ Main: Archivo Excel encontrado")

# #         self.color_teal = ft.Colors.GREY_300

# #         self._initialize_ui_components()
# #         self.content = self.resp_container
        
# #         self.inicializar_alertas_view()

# #     def _crear_boton_navegacion_profesional(self, texto, icono, index):
# #         """Crea un botón de navegación con diseño profesional y badge de notificaciones"""
        
# #         # Contenedor para el contenido del botón (icono + texto)
# #         contenido_boton = ft.Row(
# #             alignment=ft.MainAxisAlignment.CENTER,
# #             vertical_alignment=ft.CrossAxisAlignment.CENTER,
# #             spacing=15,
# #             controls=[
# #                 ft.Icon(icono, color=self.color_texto_secundario, size=22),
# #                 ft.Text(
# #                     texto, 
# #                     color=self.color_texto,
# #                     weight=ft.FontWeight.W_600,
# #                     size=14
# #                 )
# #             ]
# #         )
        
# #         # Crear el botón principal
# #         boton_principal = ft.Container(
# #             width=160,
# #             height=60,
# #             bgcolor=ft.Colors.WHITE,
# #             border_radius=10,
# #             border=ft.border.all(1, self.color_borde),
# #             alignment=ft.alignment.center,
# #             clip_behavior=ft.ClipBehavior.HARD_EDGE,
# #             animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
# #             on_hover=lambda e: self._on_hover_boton_nav(e, index),
# #             on_click=lambda e: self.change_page_manual(index),
# #         )
        
# #         # Si es el botón de Alertas, agregar el badge
# #         if index == 2:
# #             # Crear el badge
# #             badge = ft.Container(
# #                 width=20,
# #                 height=20,
# #                 border_radius=10,
# #                 bgcolor=ft.Colors.RED_600,
# #                 alignment=ft.alignment.center,
# #                 visible=False,
# #                 content=ft.Text(
# #                     "0",
# #                     size=10,
# #                     color=ft.Colors.WHITE,
# #                     weight=ft.FontWeight.BOLD
# #                 )
# #             )
            
# #             # Guardar referencia al badge
# #             self.notificacion_badge = badge
            
# #             # Crear el Stack con el botón y el badge
# #             stack_content = ft.Stack(
# #                 controls=[
# #                     # El contenido del botón (centrado)
# #                     ft.Container(
# #                         content=contenido_boton,
# #                         alignment=ft.alignment.center,
# #                         width=160,
# #                         height=60,
# #                     ),
# #                     # El badge posicionado en la esquina superior derecha
# #                     badge
# #                 ],
# #                 width=170,
# #                 height=65,
# #             )
            
# #             # Configurar el badge para que esté en la esquina superior derecha
# #             badge.top = 0
# #             badge.right = 0
            
# #             boton_principal.content = stack_content
# #             return boton_principal
# #         else:
# #             # Para otros botones, contenido simple
# #             boton_principal.content = contenido_boton
# #             return boton_principal

# #     def _on_hover_boton_nav(self, e, index):
# #         """Maneja el hover de los botones de navegación"""
# #         ctrl = e.control
# #         is_hover = (e.data == "true" or e.data is True)
        
# #         # Determinar qué botón está activo
# #         botones = [self.btn_connect, self.btn_connect2, self.btn_connect3, self.btn_connect4]
# #         index_activo = self.container_list_1.index(self.container_1.content) if self.container_1.content in self.container_list_1 else 0
        
# #         # Si no es el botón activo
# #         if index != index_activo:
# #             if is_hover:
# #                 ctrl.bgcolor = f"{self.color_primario}10"  # 10% de opacidad
# #                 ctrl.border = ft.border.all(1, self.color_primario)
# #                 ctrl.scale = ft.Scale(1.02)
                
# #                 # Obtener el contenido del botón (diferente para botón con Stack)
# #                 contenido = ctrl.content
                
# #                 # Si es el botón de Alertas (con Stack)
# #                 if index == 2 and isinstance(contenido, ft.Stack):
# #                     # El contenido está en el primer elemento del Stack (índice 0)
# #                     boton_container = contenido.controls[0]
# #                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
# #                         row_controls = boton_container.content.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_primario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_primario
# #                 else:
# #                     # Para botones normales
# #                     if isinstance(contenido, ft.Row):
# #                         row_controls = contenido.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_primario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_primario
# #             else:
# #                 ctrl.bgcolor = ft.Colors.WHITE
# #                 ctrl.border = ft.border.all(1, self.color_borde)
# #                 ctrl.scale = ft.Scale(1.0)
                
# #                 # Obtener el contenido del botón
# #                 contenido = ctrl.content
                
# #                 # Si es el botón de Alertas (con Stack)
# #                 if index == 2 and isinstance(contenido, ft.Stack):
# #                     boton_container = contenido.controls[0]
# #                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
# #                         row_controls = boton_container.content.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_texto_secundario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_texto
# #                 else:
# #                     # Para botones normales
# #                     if isinstance(contenido, ft.Row):
# #                         row_controls = contenido.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_texto_secundario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_texto
        
# #         # Usar try-except para evitar errores si la página no está lista
# #         try:
# #             ctrl.update()
# #         except:
# #             pass

# #     def inicializar_alertas_view(self):
# #         """Inicializa AlertasView después de que todo esté listo"""
# #         self.alertas_view = AlertasView(self.sistema_alertas, self.page)
# #         self.actualizar_alertas_container()
        
# #         # Inicializar el contador de alertas DESPUÉS de que la página esté lista
# #         self.page.run_thread(self.inicializar_contador_alertas)

# #     def inicializar_contador_alertas(self):
# #         """Inicializa el contador de alertas después de que la página esté lista"""
# #         time.sleep(0.5)
# #         self.actualizar_contador_alertas()

# #     def actualizar_alertas_container(self):
# #         """Actualiza el contenedor de ALERTAS con el AlertasView"""
# #         if self.alertas_view is None:
# #             return
            
# #         self.calendar_container_1.content = ft.Column(
# #             expand=True,
# #             controls=[
# #                 ft.Container(
# #                     padding=10,
# #                     bgcolor=ft.Colors.WHITE,
# #                     border_radius=10,
# #                     shadow=ft.BoxShadow(
# #                         spread_radius=1,
# #                         blur_radius=5,
# #                         color=ft.Colors.GREY_300,
# #                     ),
# #                     content=ft.Row(
# #                         alignment=ft.MainAxisAlignment.CENTER,
# #                         controls=[
# #                             ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, color=ft.Colors.RED_700, size=28),
# #                             ft.Text(
# #                                 "Historial de Alertas del Sistema",
# #                                 size=20,
# #                                 weight=ft.FontWeight.BOLD,
# #                                 color=ft.Colors.BLUE_900
# #                             ),
# #                         ],
# #                         spacing=15
# #                     )
# #                 ),
# #                 ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
# #                 ft.Container(
# #                     expand=True,
# #                     bgcolor=ft.Colors.WHITE,
# #                     border_radius=15,
# #                     padding=10,
# #                     shadow=ft.BoxShadow(
# #                         spread_radius=1,
# #                         blur_radius=5,
# #                         color=ft.Colors.GREY_300,
# #                     ),
# #                     content=self.alertas_view
# #                 )
# #             ]
# #         )

# #     def actualizar_contador_alertas(self):
# #         """Actualiza el contador de alertas en el badge"""
# #         if self.notificacion_badge is not None:
# #             total_alertas = self.sistema_alertas.contar_alertas()
            
# #             # NO mostrar el badge si estamos en la página de Alertas
# #             if total_alertas > 0 and not self.en_pagina_alertas:
# #                 self.notificacion_badge.visible = True
# #                 self.notificacion_badge.content.value = str(total_alertas) if total_alertas <= 99 else "99+"
                
# #                 # Si hay muchas alertas, hacer el badge más pequeño
# #                 if total_alertas > 9:
# #                     self.notificacion_badge.width = 24
# #                     self.notificacion_badge.height = 20
# #                 else:
# #                     self.notificacion_badge.width = 20
# #                     self.notificacion_badge.height = 20
# #             else:
# #                 self.notificacion_badge.visible = False
            
# #             # Actualizar el badge de forma segura
# #             try:
# #                 self.notificacion_badge.update()
# #             except Exception as e:
# #                 print(f"Error actualizando badge: {e}")

# #     def agregar_alerta_y_actualizar(self, causa, pagina):
# #         """Agrega una alerta y actualiza la vista y el contador"""
# #         # Agregar la alerta al sistema
# #         self.sistema_alertas.agregar_alerta(causa, pagina)
        
# #         # Actualizar el contador de notificaciones
# #         self.actualizar_contador_alertas()
        
# #         # Notificar a AlertasView si está en la página actual
# #         if self.alertas_view is not None and hasattr(self.alertas_view, 'en_pagina') and self.alertas_view.en_pagina:
# #             self.page.run_thread(self.alertas_view.cargar_ui)
# #             print(f"✓ Alerta agregada y vista actualizada: {causa}")

# #     def registrar_manual(self, e=None):
# #         """Registra un dato manualmente desde el botón en Home"""
# #         print("Registro manual solicitado")
# #         datos_actuales = self.obtener_datos_actuales_redondeados()
        
# #         registro = self.reloj_global.agregar_al_historial(
# #             datos_actuales, 
# #             tipo="registro_manual", 
# #             fuente="Manual (Home)"
# #         )
        
# #         self.agregar_alerta_y_actualizar(
# #             causa="Registro manual ejecutado desde Home",
# #             pagina="UMA"
# #         )
        
# #         self.mostrar_notificacion("✓ Registro manual agregado", ft.Colors.GREEN)
    
# #     def limpiar_historial_completamente(self, e=None):
# #         """Limpia todo el historial"""
# #         def confirmar_limpieza(e):
# #             self.reloj_global.limpiar_historial()
# #             dlg_modal.open = False
# #             self.page.update()
# #             self.mostrar_notificacion("✓ Historial limpiado", ft.Colors.GREEN)
            
# #             self.agregar_alerta_y_actualizar(
# #                 causa="Historial de registros limpiado",
# #                 pagina="UMA"
# #             )
        
# #         def cancelar_limpieza(e):
# #             dlg_modal.open = False
# #             self.page.update()
        
# #         dlg_modal = ft.AlertDialog(
# #             modal=True,
# #             title=ft.Text("Confirmar limpieza"),
# #             content=ft.Text("¿Está seguro que desea eliminar TODOS los registros del historial?\nEsta acción no se puede deshacer."),
# #             actions=[
# #                 ft.TextButton("Cancelar", on_click=cancelar_limpieza),
# #                 ft.ElevatedButton(
# #                     "Limpiar Todo", 
# #                     on_click=confirmar_limpieza,
# #                     bgcolor=ft.Colors.RED,
# #                     color=ft.Colors.WHITE
# #                 ),
# #             ],
# #             actions_alignment=ft.MainAxisAlignment.END,
# #         )
        
# #         self.page.dialog = dlg_modal
# #         dlg_modal.open = True
# #         self.page.update()
    
# #     def mostrar_notificacion(self, mensaje, color):
# #         """Muestra una notificación temporal"""
# #         snackbar = ft.SnackBar(
# #             content=ft.Text(mensaje, color=ft.Colors.WHITE),
# #             bgcolor=color,
# #             duration=2000,
# #         )
# #         self.page.snack_bar = snackbar
# #         snackbar.open = True
# #         self.page.update()

# #     def mostrar_banner_inicio(self):
# #         self.banner.open = True
# #         self.page.update()

# #     def cerrar_banner(self, e):
# #         self.banner.open = False
# #         self.page.update()

# #     def _on_alarma(self, hora):
# #         """Se ejecuta cuando el reloj global detecta una alarma"""
# #         print(f"UI: Alarma recibida: {hora}")
        
# #         datos_actuales = self.obtener_datos_actuales_redondeados()
        
# #         if hasattr(self, 'excel_manager'):
# #             self.excel_manager.guardar_todos(datos_actuales)
            
# #         registro = self.reloj_global.agregar_al_historial(
# #             datos_actuales, 
# #             tipo="registro_automatico", 
# #             fuente=f"Alarma {hora}"
# #         )
        
# #         self.agregar_alerta_y_actualizar(
# #             causa=f"Registro automático ejecutado a las {hora}",
# #             pagina="Reloj Global"
# #         )
        
# #         # FORZAR ACTUALIZACIÓN DE UMA INMEDIATAMENTE
# #         if hasattr(self, 'uma_instance'):
# #             self.page.run_thread(lambda: self.uma_instance.actualizar_lista())
        
# #         # Si estamos en la página de gráficas, actualizar
# #         if self.container_1.content == self.grafica_container and self.manometro_numero is not None:
# #             self.page.run_thread(self.actualizar_historial_manometro)
        
# #         self.mostrar_notificacion(f"✓ Registro automático a las {hora}", ft.Colors.BLUE)

# #     def obtener_datos_actuales_redondeados(self):
# #         """Obtiene los datos actuales redondeados"""
# #         datos = self.datos_tiempo_real.copy()
# #         datos['temperatura'] = round(datos['temperatura'], 1)
# #         datos['humedad'] = round(datos['humedad'])
# #         datos['presion1'] = round(datos['presion1'], 1)
# #         datos['presion2'] = round(datos['presion2'], 1)
# #         datos['presion3'] = round(datos['presion3'], 1)
# #         return datos

# #     def _initialize_ui_components(self):
# #         """Inicializa todos los componentes de la interfaz de usuario"""

# #         # 1. Crear controles de texto para UMA
# #         self.txt_temp_home = ft.Text("-- °C", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
# #         self.txt_hum_home = ft.Text("-- %", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
# #         self.txt_pres_home = ft.Text("-- Pa", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
        
# #         # 2. Crear UMA
# #         self.uma_instance = UMA(
# #             txt_temp=self.txt_temp_home,
# #             txt_hum=self.txt_hum_home,
# #             txt_pres=self.txt_pres_home,
# #             page=self.page,
# #             reloj_global=self.reloj_global
# #         )

# #         # 3. Crear manómetros CON CALLBACKS
# #         self.blue_box_presion1 = BlueBox(
# #             texto_titulo="MANOMETRO 1",
# #             texto=f"{self.datos_tiempo_real['presion1']} Pa", 
# #             mostrar_boton=False,
# #             on_grafica_click=self.abrir_pagina_grafica
# #         )
        
# #         self.blue_box_presion2 = BlueBox(
# #             texto_titulo="MANOMETRO 2",
# #             texto=f"{self.datos_tiempo_real['presion2']} Pa", 
# #             mostrar_boton=False,
# #             on_grafica_click=self.abrir_pagina_grafica
# #         )
        
# #         self.blue_box_presion3 = BlueBox(
# #             texto_titulo="MANOMETRO 3",
# #             texto=f"{self.datos_tiempo_real['presion3']} Pa", 
# #             mostrar_boton=False,
# #             on_grafica_click=self.abrir_pagina_grafica
# #         )
        
# #         self.blue_boxes = {
# #             'presion1': self.blue_box_presion1,
# #             'presion2': self.blue_box_presion2,
# #             'presion3': self.blue_box_presion3,
# #         }

# #         self.config_container = ConfiguracionContainer(self.page, self.reloj_global)

# #         ################################### PAGINA 1 (UMA) ####################################
# #         self.home_container_1 = ft.Container(
# #             bgcolor=self.color_teal,
# #             border_radius=20,
# #             expand=True,
# #             padding=20,
# #             alignment=ft.alignment.center,
# #             content=ft.Column(
# #                 expand=True,
# #                 controls=[
# #                     self.uma_instance,
# #                 ]
# #             )
# #         )

# #         ################################### PAGINA 2 (MANOMETROS) ####################################
# #         self.location_container_1 = ft.Container(
# #             bgcolor=self.color_teal,
# #             border_radius=20,
# #             expand=True,
# #             padding=20,
# #             content=ft.Column(
# #                 alignment=ft.MainAxisAlignment.START,
# #                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                 expand=True,
# #                 controls=[
# #                     ft.Container(
# #                         expand=True,
# #                         bgcolor=ft.Colors.WHITE,
# #                         border_radius=20,
# #                         alignment=ft.alignment.center,
# #                         padding=20,
# #                         shadow=ft.BoxShadow(
# #                             spread_radius=1,
# #                             blur_radius=10,
# #                             color=ft.Colors.GREY_300,
# #                         ),
# #                         content=ft.Column(
# #                             scroll=ft.ScrollMode.AUTO,
# #                             spacing=30,
# #                             controls=[
# #                                 ft.Row(
# #                                     alignment=ft.MainAxisAlignment.CENTER,
# #                                     vertical_alignment=ft.CrossAxisAlignment.CENTER,
# #                                     spacing=30,
# #                                     controls=[
# #                                         self.blue_box_presion1,
# #                                         self.blue_box_presion2,
# #                                         self.blue_box_presion3,
# #                                     ]
# #                                 )
# #                             ]
# #                         )
# #                     )
# #                 ]
# #             )
# #         )

# #         ################################### PAGINA 3 (ALERTAS) ####################################
# #         self.calendar_container_1 = ft.Container(
# #             bgcolor=self.color_teal,
# #             border_radius=20,
# #             expand=True,
# #             padding=20,
# #             content=ft.Container()
# #         )

# #         ################################### PAGINA 4 (CONFIGURACION) ####################################
# #         self.setting_container_1 = ft.Container(
# #             bgcolor=self.color_teal,
# #             border_radius=20,
# #             expand=True,
# #             padding=20,
# #             content=ft.Column(
# #                 alignment=ft.MainAxisAlignment.CENTER,
# #                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                 expand=True,
# #                 controls=[self.config_container]
# #             )
# #         )

# #         ################################### PÁGINA 5 (GRÁFICAS) ####################################
# #         # Los textos que se actualizarán dinámicamente
# #         self.titulo_grafica_text = ft.Text(
# #             value="Gráfica del Manómetro",
# #             size=24,
# #             weight=ft.FontWeight.BOLD,
# #             color=ft.Colors.BLUE_900
# #         )
        
# #         # ¡IMPORTANTE! Este Text mostrará el valor ACTUAL en tiempo real
# #         self.presion_actual_display = ft.Text(
# #             value="-- Pa",  # Valor inicial
# #             size=20,
# #             weight=ft.FontWeight.BOLD,
# #             color=ft.Colors.GREEN_700
# #         )
        
# #         # Gráfica
# #         self.grafica_chart = ft.LineChart(
# #             expand=True,
# #             tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
# #             border=ft.border.all(1, ft.Colors.GREY_300),
# #             horizontal_grid_lines=ft.ChartGridLines(
# #                 interval=1, color=ft.Colors.GREY_300, width=1
# #             ),
# #             vertical_grid_lines=ft.ChartGridLines(
# #                 interval=1, color=ft.Colors.GREY_300, width=1
# #             ),
# #             left_axis=ft.ChartAxis(
# #                 labels_size=40,
# #                 title=ft.Text("Presión (Pa)", size=12)
# #             ),
# #             bottom_axis=ft.ChartAxis(
# #                 labels_size=40,
# #                 title=ft.Text("Fecha y Hora", size=12)
# #             ),
# #             min_y=80,
# #             max_y=110,
# #         )
        
# #         # Línea de la gráfica
# #         self.linea_grafica = ft.LineChartData(
# #             color=ft.Colors.BLUE_700,
# #             stroke_width=2,
# #             curved=True,
# #             stroke_cap_round=True,
# #             below_line_gradient=ft.LinearGradient(
# #                 begin=ft.alignment.top_center,
# #                 end=ft.alignment.bottom_center,
# #                 colors=[
# #                     ft.Colors.with_opacity(0.25, ft.Colors.BLUE),
# #                     "transparent",
# #                 ],
# #             ),
# #         )
        
# #         # Lista de historial para gráficas
# #         self.lista_historial_grafica = ft.ListView(
# #             expand=True,
# #             spacing=5,
# #             padding=10
# #         )
        
# #         # Contador de registros
# #         self.contador_registros = ft.Text(
# #             "0 registros",
# #             size=14,
# #             color=ft.Colors.GREY_600
# #         )
        
# #         # Botón de actualizar
# #         self.btn_actualizar_grafica = ft.IconButton(
# #             icon=ft.Icons.REFRESH,
# #             icon_color=ft.Colors.BLUE_600,
# #             tooltip="Actualizar gráfica",
# #             on_click=lambda e: self.actualizar_historial_manometro()
# #         )
        
# #         self.grafica_container = ft.Container(
# #             bgcolor=self.color_teal,
# #             border_radius=20,
# #             expand=True,
# #             padding=20,
# #             content=ft.Column(
# #                 expand=True,
# #                 spacing=20,
# #                 controls=[
# #                     # CABECERA
# #                     ft.Container(
# #                         padding=ft.padding.symmetric(vertical=10, horizontal=15),
# #                         bgcolor=ft.Colors.WHITE,
# #                         border_radius=10,
# #                         shadow=ft.BoxShadow(
# #                             spread_radius=1,
# #                             blur_radius=5,
# #                             color=ft.Colors.GREY_300,
# #                         ),
# #                         content=ft.Row(
# #                             alignment=ft.MainAxisAlignment.START,
# #                             vertical_alignment=ft.CrossAxisAlignment.CENTER,
# #                             spacing=20,
# #                             controls=[
# #                                 ft.IconButton(
# #                                     icon=ft.Icons.ARROW_BACK,
# #                                     icon_color=ft.Colors.BLUE_700,
# #                                     icon_size=28,
# #                                     on_click=lambda e: self.change_page_manual(1),
# #                                     tooltip="Volver a Manómetros"
# #                                 ),
# #                                 self.titulo_grafica_text,
# #                                 self.btn_actualizar_grafica
# #                             ]
# #                         )
# #                     ),
                    
# #                     # CONTENIDO PRINCIPAL
# #                     ft.Container(
# #                         expand=True,
# #                         bgcolor=ft.Colors.WHITE,
# #                         border_radius=15,
# #                         padding=25,
# #                         shadow=ft.BoxShadow(
# #                             spread_radius=1,
# #                             blur_radius=10,
# #                             color=ft.Colors.GREY_300,
# #                         ),
# #                         content=ft.Row(
# #                             expand=True,
# #                             spacing=20,
# #                             controls=[
# #                                 # Panel izquierdo - Grafica
# #                                 ft.Container(
# #                                     expand=2,  # 2/3 del espacio
# #                                     padding=20,
# #                                     bgcolor=ft.Colors.WHITE,
# #                                     border_radius=10,
# #                                     content=ft.Column(
# #                                         expand=True,
# #                                         spacing=10,
# #                                         controls=[
# #                                             ft.Row(
# #                                                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                                                 controls=[
# #                                                     ft.Text("Gráfica de Presión", 
# #                                                         size=18, weight=ft.FontWeight.BOLD),
# #                                                     self.contador_registros
# #                                                 ]
# #                                             ),
                                            
# #                                             ft.Divider(height=1, color=ft.Colors.GREY_300),
                                            
# #                                             # Gráfica
# #                                             ft.Container(
# #                                                 expand=True,
# #                                                 border=ft.border.all(1, ft.Colors.GREY_300),
# #                                                 border_radius=10,
# #                                                 padding=10,
# #                                                 content=self.grafica_chart
# #                                             ),
                                            
# #                                             # Info adicional
# #                                             ft.Container(
# #                                                 padding=10,
# #                                                 bgcolor=ft.Colors.BLUE_50,
# #                                                 border_radius=5,
# #                                                 content=ft.Row(
# #                                                     spacing=10,
# #                                                     controls=[
# #                                                         ft.Text("Presión actual:", size=14, color=ft.Colors.GREY_600),
# #                                                         self.presion_actual_display,
# #                                                     ]
# #                                                 )
# #                                             )
# #                                         ]
# #                                     )
# #                                 ),
# #                                 # Panel derecho - Historial
# #                                 ft.Container(
# #                                     expand=1,  # 1/3 del espacio
# #                                     padding=20,
# #                                     bgcolor=ft.Colors.WHITE,
# #                                     border_radius=10,
# #                                     content=ft.Column(
# #                                         expand=True,
# #                                         spacing=10,
# #                                         controls=[
# #                                             ft.Row(
# #                                                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
# #                                                 controls=[
# #                                                     ft.Text("Historial de Registros", 
# #                                                         size=18, weight=ft.FontWeight.BOLD),
# #                                                 ]
# #                                             ),
# #                                             # ENCABEZADO DE TABLA
# #                                             ft.Container(
# #                                                 padding=10,
# #                                                 bgcolor=ft.Colors.BLUE_100,
# #                                                 border_radius=5,
# #                                                 margin=ft.margin.only(bottom=5),
# #                                                 content=ft.Row([
# #                                                     ft.Container(
# #                                                         width=80,
# #                                                         content=ft.Text("Presión", 
# #                                                                     weight=ft.FontWeight.BOLD,
# #                                                                     color=ft.Colors.BLUE_800,
# #                                                                     size=12)
# #                                                     ),
# #                                                     ft.Container(
# #                                                         width=80,
# #                                                         content=ft.Text("Fecha", 
# #                                                                     weight=ft.FontWeight.BOLD,
# #                                                                     color=ft.Colors.BLUE_800,
# #                                                                     size=12)
# #                                                     ),
# #                                                     ft.Container(
# #                                                         width=60,
# #                                                         content=ft.Text("Hora", 
# #                                                                     weight=ft.FontWeight.BOLD,
# #                                                                     color=ft.Colors.BLUE_800,
# #                                                                     size=12)
# #                                                     ),
# #                                                     ft.Container(
# #                                                         width=60,
# #                                                         content=ft.Text("Tipo", 
# #                                                                     weight=ft.FontWeight.BOLD,
# #                                                                     color=ft.Colors.BLUE_800,
# #                                                                     size=12)
# #                                                     ),
# #                                                 ])
# #                                             ),
                                            
# #                                             ft.Divider(height=1, color=ft.Colors.GREY_300),
                                            
# #                                             # Área de historial
# #                                             ft.Container(
# #                                                 expand=True,
# #                                                 border=ft.border.all(1, ft.Colors.GREY_300),
# #                                                 border_radius=10,
# #                                                 padding=10,
# #                                                 content=self.lista_historial_grafica
# #                                             ),
                                            
# #                                             # Leyenda
# #                                             ft.Container(
# #                                                 padding=10,
# #                                                 content=ft.Row(
# #                                                     spacing=15,
# #                                                     alignment=ft.MainAxisAlignment.CENTER,
# #                                                     controls=[
# #                                                         ft.Row([
# #                                                             ft.Container(width=12, height=12, 
# #                                                                     bgcolor=ft.Colors.BLUE_50, 
# #                                                                     border_radius=6),
# #                                                             ft.Text("Automático", size=10),
# #                                                         ]),
# #                                                         ft.Row([
# #                                                             ft.Container(width=12, height=12, 
# #                                                                     bgcolor=ft.Colors.GREEN_50, 
# #                                                                     border_radius=6),
# #                                                             ft.Text("Manual", size=10),
# #                                                         ]),
# #                                                     ]
# #                                                 )
# #                                             )
# #                                         ]
# #                                     )
# #                                 )
# #                             ]
# #                         )
# #                     )
# #                 ]
# #             )
# #         )

# #         # NUEVO: Agregar la página de gráficas a la lista
# #         self.container_list_1 = [
# #             self.home_container_1,      # índice 0: UMA
# #             self.location_container_1,  # índice 1: Manómetros  
# #             self.calendar_container_1,  # índice 2: Alertas
# #             self.setting_container_1,   # índice 3: Configuración
# #             self.grafica_container      # NUEVO índice 4: Gráficas
# #         ]

# #         self.container_1 = ft.Container(
# #             content=self.container_list_1[0], 
# #             expand=True,
# #             animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
# #         )

# #         # ========== BARRA DE NAVEGACIÓN PROFESIONAL ==========
# #         # Botones de navegación con diseño profesional
# #         self.btn_connect = self._crear_boton_navegacion_profesional("UMA", ft.Icons.MONITOR_HEART, 0)
# #         self.btn_connect2 = self._crear_boton_navegacion_profesional("Manómetros", ft.Icons.SPEED, 1)
# #         self.btn_connect3 = self._crear_boton_navegacion_profesional("Alertas", ft.Icons.NOTIFICATIONS, 2)
# #         self.btn_connect4 = self._crear_boton_navegacion_profesional("Configuración", ft.Icons.SETTINGS, 3)

# #         # Barra lateral de navegación profesional
# #         self.navigation_container = ft.Container(
# #             col=2,
# #             expand=True,
# #             bgcolor=ft.Colors.WHITE,
# #             border_radius=0,
# #             border=ft.border.only(right=ft.border.BorderSide(1, self.color_borde)),
# #             padding=ft.padding.symmetric(vertical=30, horizontal=20),
# #             shadow=ft.BoxShadow(
# #                 spread_radius=0,
# #                 blur_radius=20,
# #                 color="rgba(39, 245, 180, 0.08)",
# #                 offset=ft.Offset(5, 0)
# #             ),
# #             content=ft.Column(
# #                 alignment=ft.MainAxisAlignment.START,
# #                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                 expand=True,
# #                 spacing=15,
# #                 controls=[
# #                     # Logo y nombre
# #                     ft.Container(
# #                         padding=ft.padding.only(bottom=30),
# #                         content=ft.Column(
# #                             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                             spacing=10,
# #                             controls=[
# #                                 ft.Container(
# #                                     width=60,
# #                                     height=60,
# #                                     border_radius=15,
# #                                     bgcolor=self.color_primario,
# #                                     alignment=ft.alignment.center,
# #                                     shadow=ft.BoxShadow(
# #                                         spread_radius=0,
# #                                         blur_radius=15,
# #                                         color="rgba(39, 245, 180, 0.15)",
# #                                     ),
# #                                     content=ft.Icon(
# #                                         ft.Icons.MONITOR_HEART,
# #                                         color=ft.Colors.WHITE,
# #                                         size=30
# #                                     )
# #                                 ),
# #                                 ft.Column(
# #                                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                                     spacing=2,
# #                                     controls=[
# #                                         ft.Text(
# #                                             "Sistema de",
# #                                             size=14,
# #                                             weight=ft.FontWeight.BOLD,
# #                                             color=self.color_texto
# #                                         ),
# #                                         ft.Text(
# #                                             "Monitoreo",
# #                                             size=14,
# #                                             weight=ft.FontWeight.BOLD,
# #                                             color=self.color_primario
# #                                         )
# #                                     ]
# #                                 )
# #                             ]
# #                         )
# #                     ),
                    
# #                     ft.Divider(height=20, color=self.color_borde),
                    
# #                     # Botones de navegación
# #                     self.btn_connect,
# #                     self.btn_connect2,
# #                     self.btn_connect3,
# #                     self.btn_connect4,
                    
# #                     ft.Divider(height=30, color=self.color_borde),
                    
# #                     # Estado del sistema
# #                     ft.Container(
# #                         padding=15,
# #                         bgcolor=f"{self.color_primario}08",
# #                         border_radius=10,
# #                         content=ft.Column(
# #                             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                             spacing=8,
# #                             controls=[
# #                                 ft.Row(
# #                                     spacing=8,
# #                                     controls=[
# #                                         ft.Container(
# #                                             width=10,
# #                                             height=10,
# #                                             border_radius=5,
# #                                             bgcolor=self.color_primario
# #                                         ),
# #                                         ft.Text(
# #                                             "Sistema Activo",
# #                                             size=12,
# #                                             weight=ft.FontWeight.W_600,
# #                                             color=self.color_texto
# #                                         )
# #                                     ]
# #                                 ),
# #                                 ft.Text(
# #                                     datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
# #                                     size=11,
# #                                     color=self.color_texto_secundario
# #                                 )
# #                             ]
# #                         )
# #                     )
# #                 ]
# #             )
# #         )

# #         # Área principal de contenido
# #         self.frame_2 = ft.Container(
# #             col=10,
# #             alignment=ft.alignment.center,
# #             bgcolor=self.color_teal,
# #             expand=True,
# #             content=ft.Column(
# #                 expand=True,
# #                 controls=[
# #                     self.container_1,
# #                 ]
# #             )   
# #         )
        
# #         # Layout principal
# #         self.resp_container = ft.ResponsiveRow(
# #             vertical_alignment=ft.CrossAxisAlignment.STRETCH,
# #             controls=[
# #                 self.navigation_container,
# #                 self.frame_2,
# #             ]
# #         )

# #         self.iniciar_home_random()
        
# #         # Inicializar botón activo
# #         self.actualizar_colores_botones(0)

# #     def redondear_entero_desde_6(self, valor):
# #         """Redondea hacia arriba desde 0.6"""
# #         parte_entera = int(valor)
# #         decimal = valor - parte_entera
# #         return parte_entera + 1 if decimal >= 0.6 else parte_entera
    
# #     def generar_datos_random(self):
# #         """Genera datos aleatorios con verificación de alertas"""
# #         temp_original = random.uniform(15, 35)
# #         hum_original = random.uniform(30, 90)
# #         pres1_original = random.uniform(80, 110)
# #         pres2_original = random.uniform(80, 110)
# #         pres3_original = random.uniform(80, 110)

# #         temp = self.redondear_entero_desde_6(temp_original)
# #         hum = self.redondear_entero_desde_6(hum_original)
# #         pres1 = self.redondear_entero_desde_6(pres1_original)
# #         pres2 = self.redondear_entero_desde_6(pres2_original)
# #         pres3 = self.redondear_entero_desde_6(pres3_original)

# #         self.datos_tiempo_real = {
# #             'temperatura': temp,
# #             'humedad': hum, 
# #             'presion1': pres1,
# #             'presion2': pres2,
# #             'presion3': pres3,
# #         }

# #         # Actualizar manómetros
# #         for key, box in self.blue_boxes.items():
# #             if hasattr(box, 'actualizar_valor'):
# #                 valor = self.datos_tiempo_real[key]
# #                 box.actualizar_valor(f"{valor} Pa")

# #         # Verificar alertas - usar el nuevo método
# #         if temp > 30:
# #             self.agregar_alerta_y_actualizar(
# #                 causa=f"Temperatura CRÍTICA: {temp}°C (supera 30°C)",
# #                 pagina="UMA"
# #             )
        
# #         if hum > 85:
# #             self.agregar_alerta_y_actualizar(
# #                 causa=f"Humedad ALTA: {hum}% (superior a 85%)",
# #                 pagina="UMA"
# #             )
        
# #         if pres1 > 108:
# #             self.agregar_alerta_y_actualizar(
# #                 causa=f"Presión ALTA: {pres1}Pa (supera 108 Pa)",
# #                 pagina="UMA"
# #             )
        
# #         if pres2 > 108:
# #             self.agregar_alerta_y_actualizar(
# #                 causa=f"Presión ALTA: {pres2}Pa (supera 108 Pa)",
# #                 pagina="UMA"
# #             )
        
# #         if pres3 > 108:
# #             self.agregar_alerta_y_actualizar(
# #                 causa=f"Presión ALTA: {pres3}Pa (supera 108 Pa)",
# #                 pagina="UMA"
# #             )
        
# #         return {"presion1": pres1, "presion2": pres2, "presion3": pres3, "temperatura": temp, "humedad": hum}

# #     def iniciar_home_random(self):
# #         """Inicia la generación aleatoria de datos"""
# #         def loop():
# #             while True:
# #                 datos = self.generar_datos_random()
                
# #                 def actualizar():
# #                     # Actualiza los controles que UMA usa
# #                     self.txt_temp_home.value = f"{datos['temperatura']} °C"
# #                     self.txt_hum_home.value = f"{datos['humedad']} %"
# #                     self.txt_pres_home.value = f"{datos['presion1']} Pa"
                    
# #                     # ¡NUEVO! Actualizar también la página de gráficas si estamos en ella
# #                     if (hasattr(self, 'manometro_activo') and 
# #                         hasattr(self, 'presion_actual_display') and
# #                         self.container_1.content == self.grafica_container):
                        
# #                         # Obtener el valor directamente como dijiste
# #                         if "MANOMETRO 1" in self.manometro_activo:
# #                             self.presion_actual_display.value = f"{self.datos_tiempo_real['presion1']} Pa"
# #                         elif "MANOMETRO 2" in self.manometro_activo:
# #                             self.presion_actual_display.value = f"{self.datos_tiempo_real['presion2']} Pa"
# #                         elif "MANOMETRO 3" in self.manometro_activo:
# #                             self.presion_actual_display.value = f"{self.datos_tiempo_real['presion3']} Pa"
                    
# #                     self.page.update()
                
# #                 self.page.run_thread(actualizar)
# #                 time.sleep(2)  # Ya tienes este intervalo
        
# #         threading.Thread(target=loop, daemon=True).start()

# #     def change_page_manual(self, index):
# #         """Cambia entre páginas de la aplicación"""
# #         self.container_1.content = self.container_list_1[index]
# #         self.actualizar_colores_botones(index)
        
# #         # Actualizar estado de la página de Alertas
# #         if index == 2:  # Si estamos entrando a Alertas
# #             self.en_pagina_alertas = True
# #             # Ocultar el badge
# #             if self.notificacion_badge is not None:
# #                 self.notificacion_badge.visible = False
# #                 try:
# #                     self.notificacion_badge.update()
# #                 except:
# #                     pass
# #         else:  # Si estamos saliendo de Alertas
# #             self.en_pagina_alertas = False
# #             # Actualizar el contador para que se muestre si hay alertas
# #             self.actualizar_contador_alertas()
        
# #         # Si estamos entrando a la página de gráficas, actualizar datos
# #         if index == 4 and self.manometro_activo and self.manometro_numero:
# #             self.page.run_thread(self.actualizar_historial_manometro)
        
# #         if self.alertas_view is not None:
# #             if index == 2:  # Alertas está en índice 2
# #                 if hasattr(self.alertas_view, 'entrar_a_pagina'):
# #                     self.alertas_view.entrar_a_pagina()
# #             else:
# #                 if hasattr(self.alertas_view, 'salir_de_pagina'):
# #                     self.alertas_view.salir_de_pagina()

# #         self.page.update()
    
# #     def actualizar_colores_botones(self, index_activo):
# #         """Actualiza los colores y formas de los botones de navegación"""
# #         botones = [self.btn_connect, self.btn_connect2, self.btn_connect3, self.btn_connect4]
        
# #         for i, btn in enumerate(botones):
# #             if i == index_activo:
# #                 # Botón activo: Color primario con fondo
# #                 btn.bgcolor = self.color_primario
# #                 btn.border = ft.border.all(1, self.color_primario)
                
# #                 # Obtener el contenido del botón
# #                 contenido = btn.content
                
# #                 # Si es el botón de Alertas (con Stack)
# #                 if i == 2 and isinstance(contenido, ft.Stack):
# #                     boton_container = contenido.controls[0]
# #                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
# #                         row_controls = boton_container.content.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = ft.Colors.WHITE
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = ft.Colors.WHITE
# #                 else:
# #                     # Para botones normales
# #                     if isinstance(contenido, ft.Row):
# #                         row_controls = contenido.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = ft.Colors.WHITE
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = ft.Colors.WHITE
# #                 btn.scale = ft.Scale(1.0)
# #             else:
# #                 # Botones inactivos: Blanco con borde gris
# #                 btn.bgcolor = ft.Colors.WHITE
# #                 btn.border = ft.border.all(1, self.color_borde)
                
# #                 # Obtener el contenido del botón
# #                 contenido = btn.content
                
# #                 # Si es el botón de Alertas (con Stack)
# #                 if i == 2 and isinstance(contenido, ft.Stack):
# #                     boton_container = contenido.controls[0]
# #                     if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
# #                         row_controls = boton_container.content.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_texto_secundario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_texto
# #                 else:
# #                     # Para botones normales
# #                     if isinstance(contenido, ft.Row):
# #                         row_controls = contenido.controls
# #                         if len(row_controls) > 1:
# #                             if hasattr(row_controls[0], 'color'):
# #                                 row_controls[0].color = self.color_texto_secundario
# #                             if hasattr(row_controls[1], 'color'):
# #                                 row_controls[1].color = self.color_texto
# #                 btn.scale = ft.Scale(1.0)
        
# #         # Actualizar todos los botones de forma segura
# #         for btn in botones:
# #             try:
# #                 btn.update()
# #             except:
# #                 pass

# #     def abrir_pagina_grafica(self, titulo_manometro):
# #         """Abre la página de gráficas para un manómetro específico"""
# #         print(f"Abriendo gráfica para: {titulo_manometro}")
        
# #         # 1. Guardar referencia al manómetro activo
# #         self.manometro_activo = titulo_manometro
        
# #         # 2. Obtener datos del manómetro específico
# #         if "MANOMETRO 1" in titulo_manometro:
# #             self.manometro_numero = 1
# #             datos = self.datos_tiempo_real['presion1']
# #         elif "MANOMETRO 2" in titulo_manometro:
# #             self.manometro_numero = 2
# #             datos = self.datos_tiempo_real['presion2']
# #         elif "MANOMETRO 3" in titulo_manometro:
# #             self.manometro_numero = 3
# #             datos = self.datos_tiempo_real['presion3']
# #         else:
# #             self.manometro_numero = None
# #             datos = 0
        
# #         # 3. Actualizar el título de la página
# #         self.titulo_grafica_text.value = f"Gráfica: {titulo_manometro}"
        
# #         # 4. Actualizar el valor inicial en el display
# #         self.presion_actual_display.value = f"{datos} Pa"
        
# #         # 5. Cambiar a la página de gráficas (índice 4)
# #         self.change_page_manual(4)
        
# #         # 6. Actualizar historial y gráfica
# #         self.page.run_thread(self.actualizar_historial_manometro)
        
# #         # 7. Imprimir confirmación
# #         print(f"✓ Página de gráficas abierta para {titulo_manometro}")
# #         print(f"  Presión actual: {datos} Pa")
# #         print(f"  Número de manómetro: {self.manometro_numero}")

# #     def crear_punto_grafica(self, x, y):
# #         """Crea un punto de datos para la gráfica"""
# #         return ft.LineChartDataPoint(
# #             x,
# #             y,
# #             selected_below_line=ft.ChartPointLine(
# #                 width=0.5, color=ft.Colors.GREY_400, dash_pattern=[2, 4]
# #             ),
# #             selected_point=ft.ChartCirclePoint(
# #                 stroke_width=2, 
# #                 color=ft.Colors.BLUE_700,
# #                 radius=4
# #             ),
# #         )

# #     def actualizar_historial_manometro(self, e=None):
# #         """Actualiza la gráfica y la lista de historial para el manómetro activo"""
# #         if not self.manometro_activo or not self.manometro_numero:
# #             print("No hay manómetro activo")
# #             return
        
# #         print(f"Actualizando historial para manómetro {self.manometro_numero}")
        
# #         # Obtener registros del manómetro desde el historial principal
# #         registros = self.reloj_global.obtener_registros_por_manometro(
# #             self.manometro_numero, 
# #             limite=20
# #         )
        
# #         # Actualizar contador
# #         self.contador_registros.value = f"{len(registros)} registros"
        
# #         # Limpiar gráfica actual
# #         puntos_grafica = []
# #         self.grafica_chart.data_series = []
        
# #         if registros:
# #             # Crear etiquetas para el eje X (fechas)
# #             etiquetas_x = []
            
# #             # Agregar puntos a la gráfica (X = índice, Y = presión)
# #             # Ordenamos para que el más antiguo esté a la izquierda
# #             for i, registro in enumerate(registros):
# #                 # Usar timestamp como X para espaciar correctamente
# #                 timestamp = registro['fecha_hora'].timestamp()
# #                 punto = self.crear_punto_grafica(timestamp, registro['presion'])
# #                 puntos_grafica.append(punto)
                
# #                 # Crear etiqueta para el eje X (fecha corta)
# #                 fecha_corta = registro['fecha_hora'].strftime("%d/%m\n%H:%M")
# #                 etiquetas_x.append(ft.ChartAxisLabel(
# #                     value=timestamp,
# #                     label=ft.Text(fecha_corta, size=10)
# #                 ))
            
# #             # Configurar eje X con las etiquetas de fecha
# #             self.grafica_chart.bottom_axis = ft.ChartAxis(
# #                 labels=etiquetas_x,
# #                 labels_size=35,
# #                 labels_interval=1 if len(etiquetas_x) <= 10 else 2,
# #                 title=ft.Text("Fecha y Hora", size=12)
# #             )
            
# #             # Configurar rango Y dinámico
# #             presiones = [r['presion'] for r in registros]
# #             min_presion = min(presiones) if presiones else 80
# #             max_presion = max(presiones) if presiones else 110
            
# #             # Agregar margen
# #             self.grafica_chart.min_y = max(70, min_presion - 5)
# #             self.grafica_chart.max_y = min(120, max_presion + 5)
            
# #             # Configurar eje Y
# #             self.grafica_chart.left_axis = ft.ChartAxis(
# #                 labels_size=40,
# #                 title=ft.Text("Presión (Pa)", size=12)
# #             )
            
# #             # Actualizar línea de la gráfica
# #             self.linea_grafica.data_points = puntos_grafica
# #             self.grafica_chart.data_series = [self.linea_grafica]
        
# #         # Limpiar lista actual
# #         self.lista_historial_grafica.controls.clear()
        
# #         # Agregar registros a la lista (más reciente primero)
# #         for registro in reversed(registros):  # Invertir para mostrar más reciente arriba
# #             # Determinar color según tipo
# #             if "automatico" in registro['tipo']:
# #                 color_fondo = ft.Colors.BLUE_50
# #                 icono = ft.Icons.AUTORENEW
# #                 color_icono = ft.Colors.BLUE_600
# #             elif "manual" in registro['tipo']:
# #                 color_fondo = ft.Colors.GREEN_50
# #                 icono = ft.Icons.TOUCH_APP
# #                 color_icono = ft.Colors.GREEN_600
# #             else:
# #                 color_fondo = ft.Colors.GREY_50
# #                 icono = ft.Icons.INFO
# #                 color_icono = ft.Colors.GREY_600
            
# #             # Crear fila para la tabla
# #             fila = ft.Container(
# #                 padding=10,
# #                 bgcolor=ft.Colors.RED_50 if registro['presion'] > 108 else color_fondo,
# #                 border_radius=5,
# #                 margin=ft.margin.only(bottom=5),
# #                 content=ft.Row([
# #                     # Presión
# #                     ft.Container(
# #                         width=80,
# #                         content=ft.Text(
# #                             f"{registro['presion']} Pa",
# #                             size=12,
# #                             color=ft.Colors.RED_700 if registro['presion'] > 108 else ft.Colors.BLUE_700,
# #                             weight=ft.FontWeight.BOLD if registro['presion'] > 108 else ft.FontWeight.NORMAL
# #                         )
# #                     ),
# #                     # Fecha
# #                     ft.Container(
# #                         width=80,
# #                         content=ft.Text(
# #                             registro['fecha'],
# #                             size=12,
# #                             color=ft.Colors.GREY_700
# #                         )
# #                     ),
# #                     # Hora
# #                     ft.Container(
# #                         width=60,
# #                         content=ft.Text(
# #                             registro['hora'],
# #                             size=12,
# #                             color=ft.Colors.GREY_700
# #                         )
# #                     ),
# #                     # Tipo con icono
# #                     ft.Container(
# #                         width=60,
# #                         content=ft.Row([
# #                             ft.Icon(icono, size=14, color=color_icono),
# #                             ft.Text(
# #                                 "Auto" if "automatico" in registro['tipo'] else "Manual",
# #                                 size=10,
# #                                 color=color_icono
# #                             )
# #                         ], spacing=5)
# #                     ),
# #                 ])
# #             )
            
# #             self.lista_historial_grafica.controls.append(fila)
        
# #         # Si no hay registros, mostrar mensaje
# #         if not registros:
# #             self.lista_historial_grafica.controls.append(
# #                 ft.Container(
# #                     padding=20,
# #                     alignment=ft.alignment.center,
# #                     content=ft.Column(
# #                         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
# #                         spacing=10,
# #                         controls=[
# #                             ft.Icon(ft.Icons.HISTORY, size=48, color=ft.Colors.GREY_400),
# #                             ft.Text(
# #                                 "No hay registros históricos",
# #                                 size=14,
# #                                 color=ft.Colors.GREY_500
# #                             )
# #                         ]
# #                     )
# #                 )
# #             )
        
# #         # Actualizar todos los componentes
# #         try:
# #             self.grafica_chart.update()
# #             self.lista_historial_grafica.update()
# #             self.contador_registros.update()
# #             self.presion_actual_display.update()
# #         except Exception as e:
# #             print(f"Error actualizando componentes: {e}")

# #     def will_unmount(self):
# #         """Detener el reloj global al cerrar la app"""
# #         self.reloj_global.detener()


# # def main(page: ft.Page):
# #     page.title = "Sistema de Monitoreo Inteligente"
# #     page.window.width = 1400
# #     page.window.height = 750
# #     page.window.resizable = True
# #     page.horizontal_alignment = "center"
# #     page.vertical_alignment = "center"
# #     page.theme_mode = ft.ThemeMode.LIGHT
# #     page.window.bgcolor = ft.Colors.WHITE
# #     page.padding = 0

# #     ui = UI(page)
# #     page.add(ui)

# # if __name__ == "__main__":
# #     ft.app(target=main)






































import flet as ft
import threading
import time
import datetime
import json
import os
import random
from cajaAzul import BlueBox
from configuracion import ConfiguracionContainer
from excel5 import ExcelUnicoArchivo
from alertas import SistemaAlertas, AlertasView
from paguina1 import UMA

class RelojGlobal:
    def __init__(self):
        self.horas_registradas = []
        self.archivo_horas = "horas.json"
        self.historial_registros = []
        self.archivo_historial = "historial_registros.json"
        self.reloj_activo = True
        self.ultima_ejecucion = {}
        self.callbacks = []
        self.historial_callbacks = []
        
        # Cargar horas guardadas
        self.cargar_horas()
        self.cargar_historial()
        self.iniciar()

    def agregar_callback(self, callback):
        """Agrega una función que se ejecutará cuando suene una alarma"""
        self.callbacks.append(callback)
    
    def agregar_callback_historial(self, callback):
        """Agrega una función que se ejecutará cuando se agregue un nuevo registro al historial"""
        self.historial_callbacks.append(callback)

    def cargar_horas(self):
        """Carga las horas desde archivo JSON"""
        if os.path.exists(self.archivo_horas):
            try:
                with open(self.archivo_horas, "r") as file:
                    datos = json.load(file)
                    self.horas_registradas = [
                        datetime.datetime.strptime(h, "%H:%M").time()
                        for h in datos
                    ]
                print(f"RelojGlobal: Horas cargadas: {[h.strftime('%I:%M %p') for h in self.horas_registradas]}")
            except Exception as e:
                print(f"RelojGlobal: Error cargando horas: {e}")
                self.horas_registradas = []
    
    def cargar_historial(self):
        """Carga el historial desde archivo JSON"""
        if os.path.exists(self.archivo_historial):
            try:
                with open(self.archivo_historial, "r") as file:
                    self.historial_registros = json.load(file)
                print(f"RelojGlobal: Historial cargado ({len(self.historial_registros)} registros)")
            except Exception as e:
                print(f"RelojGlobal: Error cargando historial: {e}")
                self.historial_registros = []
        else:
            self.guardar_historial()

    def guardar_horas(self):
        """Guarda las horas en archivo JSON"""
        try:
            datos = [h.strftime("%H:%M") for h in self.horas_registradas]
            with open(self.archivo_horas, "w") as file:
                json.dump(datos, file)
        except Exception as e:
            print(f"RelojGlobal: Error guardando horas: {e}")
    
    def guardar_historial(self):
        """Guarda el historial en archivo JSON"""
        try:
            if len(self.historial_registros) > 50:
                self.historial_registros = self.historial_registros[-50:]
            
            with open(self.archivo_historial, "w") as file:
                json.dump(self.historial_registros, file, indent=2)
        except Exception as e:
            print(f"RelojGlobal: Error guardando historial: {e}")

    def agregar_hora(self, hora_time):
        """Agrega una hora a la lista global"""
        if hora_time not in self.horas_registradas:
            self.horas_registradas.append(hora_time)
            self.guardar_horas()
            print(f"RelojGlobal: Hora agregada: {hora_time.strftime('%I:%M %p')}")
            return True
        return False

    def eliminar_hora(self, hora_time):
        """Elimina una hora de la lista global"""
        if hora_time in self.horas_registradas:
            self.horas_registradas.remove(hora_time)
            self.guardar_horas()
            print(f"RelojGlobal: Hora eliminada: {hora_time.strftime('%I:%M %p')}")
            return True
        return False
    
    def agregar_al_historial(self, datos, tipo="registro_automatico", fuente="Reloj Global"):
        """Agrega un registro al historial"""
        registro = {
            "fecha": datetime.datetime.now().strftime("%d/%m/%y"),
            "hora": datetime.datetime.now().strftime("%H:%M"),
            "datos": datos,
            "tipo": tipo,
            "fuente": fuente
        }
        self.historial_registros.append(registro)
        self.guardar_historial()
        
        # Notificar a todos los callbacks
        for callback in self.historial_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"RelojGlobal: Error en callback de historial: {e}")
        
        return registro
    
    def obtener_registros_por_manometro(self, manometro_numero, limite=20):
        """
        Obtiene todos los registros históricos para un manómetro específico.
        manometro_numero: 1, 2 o 3
        limite: cantidad máxima de registros a retornar
        """
        registros_manometro = []
        
        # Filtrar registros para este manómetro (más recientes primero)
        for registro in self.historial_registros[::-1]:  # Invertir para obtener más recientes primero
            if 'datos' in registro:
                datos = registro['datos']
                # Extraer la presión del manómetro específico
                clave_presion = f'presion{manometro_numero}'
                if clave_presion in datos:
                    # Convertir fecha y hora a datetime para ordenar
                    fecha_hora_str = f"{registro['fecha']} {registro['hora']}"
                    fecha_hora = datetime.datetime.strptime(fecha_hora_str, "%d/%m/%y %H:%M")
                    
                    registro_manometro = {
                        'fecha': registro['fecha'],
                        'hora': registro['hora'],
                        'fecha_hora': fecha_hora,
                        'presion': datos[clave_presion],
                        'tipo': registro.get('tipo', 'desconocido'),
                        'fuente': registro.get('fuente', 'desconocido')
                    }
                    registros_manometro.append(registro_manometro)
            
            # Limitar cantidad de registros
            if len(registros_manometro) >= limite:
                break
        
        # Ordenar por fecha_hora (más antiguo primero para gráfica de izquierda a derecha)
        registros_manometro.sort(key=lambda x: x['fecha_hora'])
        
        return registros_manometro

    def limpiar_historial(self):
        """Limpia todo el historial"""
        self.historial_registros = []
        self.guardar_historial()
        print("RelojGlobal: Historial limpiado")
        
        # Notificar a los callbacks
        for callback in self.historial_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"RelojGlobal: Error en callback de limpieza: {e}")

    def iniciar(self):
        """Inicia el reloj global en un hilo separado"""
        if not hasattr(self, 'thread') or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()
            print("RelojGlobal: Iniciado")

    def _loop(self):
        """Loop principal del reloj"""
        while self.reloj_activo:
            try:
                ahora = datetime.datetime.now()
                
                for hora_obj in self.horas_registradas:
                    hora_actual_minuto = ahora.strftime("%I:%M %p")
                    segundos = ahora.strftime("%S")
                    hora_objetivo_str = hora_obj.strftime("%I:%M %p")

                    if hora_actual_minuto == hora_objetivo_str and segundos == "00":
                        h_obj = datetime.datetime.combine(ahora.date(), hora_obj)
                        clave = h_obj.strftime("%Y-%m-d %H:%M")

                        if clave not in self.ultima_ejecucion:
                            self.ultima_ejecucion[clave] = True
                            self._ejecutar_alarma(hora_objetivo_str)
                            print(f"RelojGlobal: ✓ Alarma: {hora_objetivo_str}")
                
                hoy = datetime.datetime.now().date()
                claves_a_eliminar = [k for k in self.ultima_ejecucion 
                                    if datetime.datetime.strptime(k.split(" ")[0], "%Y-%m-%d").date() < hoy]
                for k in claves_a_eliminar:
                    del self.ultima_ejecucion[k]

                time.sleep(1)
                
            except Exception as e:
                print(f"RelojGlobal: Error en loop: {e}")
                time.sleep(1)

    def _ejecutar_alarma(self, hora):
        """Ejecuta todos los callbacks registrados"""
        for callback in self.callbacks:
            try:
                callback(hora)
            except Exception as e:
                print(f"RelojGlobal: Error en callback: {e}")

    def detener(self):
        """Detiene el reloj global"""
        self.reloj_activo = False


class UI(ft.Container):
    def __init__(self, page):
        super().__init__(expand=True)
        self.page = page

        # Variable para verificar bandera de registro manual
        self.bandera_btn_registro = False
        
        # COLORES PARA LA BARRA DE NAVEGACIÓN
        self.color_primario = "#27F5B4"  # Verde agua
        self.color_fondo = "#FFFFFF"  # Blanco
        self.color_texto = "#2C3E50"  # Azul oscuro
        self.color_texto_secundario = "#6C757D"  # Gris
        self.color_borde = "#E9ECEF"  # Gris claro para bordes
        
        # Datos en tiempo real (manteniendo los originales)
        self.datos_tiempo_real = {
            'temperatura': 0,
            'humedad': 0, 
            'presion1': 0,
            'presion2': 0,
            'presion3': 0,
        }

        self.excel_manager = ExcelUnicoArchivo()
        self.bandera_excel = self.excel_manager.get_bandera_archivo()
        
        self.reloj_global = RelojGlobal()
        self.sistema_alertas = SistemaAlertas()
        self.alertas_view = None
        
        # Variable para el badge de notificaciones
        self.notificacion_badge = None
        # Variable para saber si estamos en la página de Alertas
        self.en_pagina_alertas = False
        
        # Variables para gráficas
        self.manometro_activo = None
        self.manometro_numero = None
        self.grafica_chart = None
        self.lista_historial_grafica = None
        self.titulo_grafica_text = None

        self.banner = ft.Banner(
            bgcolor=ft.Colors.AMBER_100,
            leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
            content=ft.Text(
                "Sistema de monitoreo iniciado",
                color=ft.Colors.BLACK,
            ),
            actions=[
                ft.TextButton("OK", on_click=self.cerrar_banner)
            ],
        )
        self.page.controls.append(self.banner)

        if not self.bandera_excel:
            print("⚠️ Main: No se encontró archivo Excel, mostrando banner...")
            self.mostrar_banner_inicio()
        else:
            self.reloj_global.agregar_callback(self._on_alarma)
            print("✅ Main: Archivo Excel encontrado")

        if self.bandera_btn_registro:
            self.reloj_global.agregar_callback(self._on_alarma)

        self.color_teal = ft.Colors.GREY_300

        self._initialize_ui_components()
        self.content = self.resp_container
        
        self.inicializar_alertas_view()

    def _crear_boton_navegacion_profesional(self, texto, icono, index):
        """Crea un botón de navegación con diseño profesional y badge de notificaciones"""
        
        # Contenedor para el contenido del botón (icono + texto)
        contenido_boton = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            controls=[
                ft.Icon(icono, color=self.color_texto_secundario, size=22),
                ft.Text(
                    texto, 
                    color=self.color_texto,
                    weight=ft.FontWeight.W_600,
                    size=14
                )
            ]
        )
        
        # Crear el botón principal
        boton_principal = ft.Container(
            width=160,
            height=60,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.border.all(1, self.color_borde),
            alignment=ft.alignment.center,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            on_hover=lambda e: self._on_hover_boton_nav(e, index),
            on_click=lambda e: self.change_page_manual(index),
        )
        
        # Si es el botón de Alertas, agregar el badge
        if index == 2:
            # Crear el badge
            badge = ft.Container(
                width=20,
                height=20,
                border_radius=10,
                bgcolor=ft.Colors.RED_600,
                alignment=ft.alignment.center,
                visible=False,
                content=ft.Text(
                    "0",
                    size=10,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD
                )
            )
            
            # Guardar referencia al badge
            self.notificacion_badge = badge
            
            # Crear el Stack con el botón y el badge
            stack_content = ft.Stack(
                controls=[
                    # El contenido del botón (centrado)
                    ft.Container(
                        content=contenido_boton,
                        alignment=ft.alignment.center,
                        width=160,
                        height=60,
                    ),
                    # El badge posicionado en la esquina superior derecha
                    badge
                ],
                width=170,
                height=65,
            )
            
            # Configurar el badge para que esté en la esquina superior derecha
            badge.top = 0
            badge.right = 0
            
            boton_principal.content = stack_content
            return boton_principal
        else:
            # Para otros botones, contenido simple
            boton_principal.content = contenido_boton
            return boton_principal

    def _on_hover_boton_nav(self, e, index):
        """Maneja el hover de los botones de navegación"""
        ctrl = e.control
        is_hover = (e.data == "true" or e.data is True)
        
        # Determinar qué botón está activo
        botones = [self.btn_connect, self.btn_connect2, self.btn_connect3, self.btn_connect4]
        index_activo = self.container_list_1.index(self.container_1.content) if self.container_1.content in self.container_list_1 else 0
        
        # Si no es el botón activo
        if index != index_activo:
            if is_hover:
                ctrl.bgcolor = f"{self.color_primario}10"  # 10% de opacidad
                ctrl.border = ft.border.all(1, self.color_primario)
                ctrl.scale = ft.Scale(1.02)
                
                # Obtener el contenido del botón (diferente para botón con Stack)
                contenido = ctrl.content
                
                # Si es el botón de Alertas (con Stack)
                if index == 2 and isinstance(contenido, ft.Stack):
                    # El contenido está en el primer elemento del Stack (índice 0)
                    boton_container = contenido.controls[0]
                    if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
                        row_controls = boton_container.content.controls
                        if len(row_controls) > 1:
                            if hasattr(row_controls[0], 'color'):
                                row_controls[0].color = self.color_primario
                            if hasattr(row_controls[1], 'color'):
                                row_controls[1].color = self.color_primario
                else:
                    # Para botones normales
                    if isinstance(contenido, ft.Row):
                        row_controls = contenido.controls
                        if len(row_controls) > 1:
                            if hasattr(row_controls[0], 'color'):
                                row_controls[0].color = self.color_primario
                            if hasattr(row_controls[1], 'color'):
                                row_controls[1].color = self.color_primario
            else:
                ctrl.bgcolor = ft.Colors.WHITE
                ctrl.border = ft.border.all(1, self.color_borde)
                ctrl.scale = ft.Scale(1.0)
                
                # Obtener el contenido del botón
                contenido = ctrl.content
                
                # Si es el botón de Alertas (con Stack)
                if index == 2 and isinstance(contenido, ft.Stack):
                    boton_container = contenido.controls[0]
                    if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
                        row_controls = boton_container.content.controls
                        if len(row_controls) > 1:
                            if hasattr(row_controls[0], 'color'):
                                row_controls[0].color = self.color_texto_secundario
                            if hasattr(row_controls[1], 'color'):
                                row_controls[1].color = self.color_texto
                else:
                    # Para botones normales
                    if isinstance(contenido, ft.Row):
                        row_controls = contenido.controls
                        if len(row_controls) > 1:
                            if hasattr(row_controls[0], 'color'):
                                row_controls[0].color = self.color_texto_secundario
                            if hasattr(row_controls[1], 'color'):
                                row_controls[1].color = self.color_texto
        
        # Usar try-except para evitar errores si la página no está lista
        try:
            ctrl.update()
        except:
            pass

    def inicializar_alertas_view(self):
        """Inicializa AlertasView después de que todo esté listo"""
        self.alertas_view = AlertasView(self.sistema_alertas, self.page)
        self.actualizar_alertas_container()
        
        # Inicializar el contador de alertas DESPUÉS de que la página esté lista
        self.page.run_thread(self.inicializar_contador_alertas)

    def inicializar_contador_alertas(self):
        """Inicializa el contador de alertas después de que la página esté lista"""
        time.sleep(0.5)
        self.actualizar_contador_alertas()

    def actualizar_alertas_container(self):
        """Actualiza el contenedor de ALERTAS con el AlertasView"""
        if self.alertas_view is None:
            return
            
        self.calendar_container_1.content = ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    padding=10,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=5,
                        color=ft.Colors.GREY_300,
                    ),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE, color=ft.Colors.RED_700, size=28),
                            ft.Text(
                                "Historial de Alertas del Sistema",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_900
                            ),
                        ],
                        spacing=15
                    )
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Container(
                    expand=True,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=15,
                    padding=10,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=5,
                        color=ft.Colors.GREY_300,
                    ),
                    content=self.alertas_view
                )
            ]
        )

    def actualizar_contador_alertas(self):
        """Actualiza el contador de alertas en el badge"""
        if self.notificacion_badge is not None:
            total_alertas = self.sistema_alertas.contar_alertas()
            
            # NO mostrar el badge si estamos en la página de Alertas
            if total_alertas > 0 and not self.en_pagina_alertas:
                self.notificacion_badge.visible = True
                self.notificacion_badge.content.value = str(total_alertas) if total_alertas <= 99 else "99+"
                
                # Si hay muchas alertas, hacer el badge más pequeño
                if total_alertas > 9:
                    self.notificacion_badge.width = 24
                    self.notificacion_badge.height = 20
                else:
                    self.notificacion_badge.width = 20
                    self.notificacion_badge.height = 20
            else:
                self.notificacion_badge.visible = False
            
            # Actualizar el badge de forma segura
            try:
                self.notificacion_badge.update()
            except Exception as e:
                print(f"Error actualizando badge: {e}")

    # def agregar_alerta_y_actualizar(self, causa, pagina):
    #     """Agrega una alerta y actualiza la vista y el contador"""
    #     # Agregar la alerta al sistema
    #     self.sistema_alertas.agregar_alerta(causa, pagina)
        
    #     # Actualizar el contador de notificaciones
    #     self.actualizar_contador_alertas()
        
    #     # Notificar a AlertasView si está en la página actual
    #     if self.alertas_view is not None and hasattr(self.alertas_view, 'en_pagina') and self.alertas_view.en_pagina:
    #         self.page.run_thread(self.alertas_view.cargar_ui)
    #         print(f"✓ Alerta agregada y vista actualizada: {causa}")

    def agregar_alerta_y_actualizar(self, causa, pagina, elemento=None, valor=None, tipo=None):
        """Agrega una alerta con información detallada"""
        # Crear mensaje detallado
        mensaje = causa
        if elemento:
            mensaje = f"[{elemento}] {causa}"
        
        # Agregar la alerta al sistema
        self.sistema_alertas.agregar_alerta(
            causa=mensaje,
            pagina=pagina,
            elemento=elemento,
            valor=valor,
            tipo=tipo
        )
        
        # Actualizar el contador de notificaciones
        self.actualizar_contador_alertas()
        
        # Notificar a AlertasView si está en la página actual
        if self.alertas_view is not None and hasattr(self.alertas_view, 'en_pagina') and self.alertas_view.en_pagina:
            self.page.run_thread(self.alertas_view.cargar_ui)
            print(f"✓ Alerta detallada agregada: {elemento} - {causa}")

    def registrar_manual(self, e=None):
        """Registra un dato manualmente desde el botón en Home"""
        print("Registro manual solicitado")
        datos_actuales = self.obtener_datos_actuales_redondeados()
        
        registro = self.reloj_global.agregar_al_historial(
            datos_actuales, 
            tipo="registro_manual", 
            fuente="Manual (Home)"
        )
        
        self.agregar_alerta_y_actualizar(
            causa="Registro manual ejecutado desde Home",
            pagina="UMA"
        )
        
        self.mostrar_notificacion("✓ Registro manual agregado", ft.Colors.GREEN)
    
    def limpiar_historial_completamente(self, e=None):
        """Limpia todo el historial"""
        def confirmar_limpieza(e):
            self.reloj_global.limpiar_historial()
            dlg_modal.open = False
            self.page.update()
            self.mostrar_notificacion("✓ Historial limpiado", ft.Colors.GREEN)
            
            self.agregar_alerta_y_actualizar(
                causa="Historial de registros limpiado",
                pagina="UMA"
            )
        
        def cancelar_limpieza(e):
            dlg_modal.open = False
            self.page.update()
        
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar limpieza"),
            content=ft.Text("¿Está seguro que desea eliminar TODOS los registros del historial?\nEsta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_limpieza),
                ft.ElevatedButton(
                    "Limpiar Todo", 
                    on_click=confirmar_limpieza,
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = dlg_modal
        dlg_modal.open = True
        self.page.update()
    
    def mostrar_notificacion(self, mensaje, color):
        """Muestra una notificación temporal"""
        snackbar = ft.SnackBar(
            content=ft.Text(mensaje, color=ft.Colors.WHITE),
            bgcolor=color,
            duration=2000,
        )
        self.page.snack_bar = snackbar
        snackbar.open = True
        self.page.update()

    def mostrar_banner_inicio(self):
        self.banner.open = True
        self.page.update()

    def cerrar_banner(self, e):
        self.banner.open = False
        self.page.update()

    def registrar_manual(self, e=None):
        """Registro manual DESDE CUALQUIER PARTE - Guarda en Excel"""
        print("📝 Ejecutando registro manual completo")
        
        # Obtener hora actual
        hora_actual = datetime.datetime.now().strftime("%I:%M %p")
        
        # Llamar a _on_alarma que ya hace TODO:
        # 1. Guarda en Excel (excel_manager.guardar_todos)
        # 2. Agrega al historial
        # 3. Crea alertas
        # 4. Actualiza vistas
        self._on_alarma(f"Manual {hora_actual}")
        
        # Notificación extra
        self.mostrar_notificacion(f"✓ Registro MANUAL completado", ft.Colors.GREEN)

    def _on_alarma(self, hora):
        """Se ejecuta cuando el reloj global detecta una alarma"""
        print(f"UI: Alarma recibida: {hora}")
        
        datos_actuales = self.obtener_datos_actuales_redondeados()
        
        if hasattr(self, 'excel_manager'):
            self.excel_manager.guardar_todos(datos_actuales)
            
        registro = self.reloj_global.agregar_al_historial(
            datos_actuales, 
            tipo="registro_automatico", 
            fuente=f"Alarma {hora}"
        )
        
        self.agregar_alerta_y_actualizar(
            causa=f"Registro automático ejecutado a las {hora}",
            pagina="Reloj Global"
        )
        
        # FORZAR ACTUALIZACIÓN DE UMA INMEDIATAMENTE
        if hasattr(self, 'uma_instance'):
            self.page.run_thread(lambda: self.uma_instance.actualizar_lista())
        
        # Si estamos en la página de gráficas, actualizar
        if self.container_1.content == self.grafica_container and self.manometro_numero is not None:
            self.page.run_thread(self.actualizar_historial_manometro)
        
        self.mostrar_notificacion(f"✓ Registro automático a las {hora}", ft.Colors.BLUE)

    def obtener_datos_actuales_redondeados(self):
        """Obtiene los datos actuales redondeados"""
        datos = self.datos_tiempo_real.copy()
        datos['temperatura'] = round(datos['temperatura'], 1)
        datos['humedad'] = round(datos['humedad'])
        datos['presion1'] = round(datos['presion1'], 1)
        datos['presion2'] = round(datos['presion2'], 1)
        datos['presion3'] = round(datos['presion3'], 1)
        return datos

    def _initialize_ui_components(self):
        """Inicializa todos los componentes de la interfaz de usuario"""

        # 1. Crear controles de texto para UMA
        self.txt_temp_home = ft.Text("-- °C", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
        self.txt_hum_home = ft.Text("-- %", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
        self.txt_pres_home = ft.Text("-- Pa", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
        
        # 2. Crear UMA
        self.uma_instance = UMA(
            txt_temp=self.txt_temp_home,
            txt_hum=self.txt_hum_home,
            txt_pres=self.txt_pres_home,
            page=self.page,
            reloj_global=self.reloj_global,
            on_registro_manual=self.registrar_manual  # ← Callback
        )

        # ¡VINCULAR EL BOTÓN DE UMA AL MÉTODO DE UI!
        # Opción A: Sobrescribir el método
        # self.uma_instance.registrar_manual = self.registrar_manual
        
        # Opción B: O modificar el botón directamente
        if hasattr(self.uma_instance, 'btn_registro'):
            self.uma_instance.btn_registro.on_click = self.registrar_manual

        # 3. Crear manómetros CON CALLBACKS
        self.blue_box_presion1 = BlueBox(
            texto_titulo="MANOMETRO 1",
            texto=f"{self.datos_tiempo_real['presion1']} Pa", 
            mostrar_boton=False,
            on_grafica_click=self.abrir_pagina_grafica
        )
        
        self.blue_box_presion2 = BlueBox(
            texto_titulo="MANOMETRO 2",
            texto=f"{self.datos_tiempo_real['presion2']} Pa", 
            mostrar_boton=False,
            on_grafica_click=self.abrir_pagina_grafica
        )
        
        self.blue_box_presion3 = BlueBox(
            texto_titulo="MANOMETRO 3",
            texto=f"{self.datos_tiempo_real['presion3']} Pa", 
            mostrar_boton=False,
            on_grafica_click=self.abrir_pagina_grafica
        )
        
        self.blue_boxes = {
            'presion1': self.blue_box_presion1,
            'presion2': self.blue_box_presion2,
            'presion3': self.blue_box_presion3,
        }

        self.config_container = ConfiguracionContainer(self.page, self.reloj_global)

        ################################### PAGINA 1 (UMA) ####################################
        self.home_container_1 = ft.Container(
            bgcolor=self.color_teal,
            border_radius=20,
            expand=True,
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Column(
                expand=True,
                controls=[
                    self.uma_instance,
                ]
            )
        )

        ################################### PAGINA 2 (MANOMETROS) ####################################
        self.location_container_1 = ft.Container(
            bgcolor=self.color_teal,
            border_radius=20,
            expand=True,
            padding=20,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                controls=[
                    ft.Container(
                        expand=True,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=20,
                        alignment=ft.alignment.center,
                        padding=20,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.Colors.GREY_300,
                        ),
                        content=ft.Column(
                            scroll=ft.ScrollMode.AUTO,
                            spacing=30,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=30,
                                    controls=[
                                        self.blue_box_presion1,
                                        self.blue_box_presion2,
                                        self.blue_box_presion3,
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )

        ################################### PAGINA 3 (ALERTAS) ####################################
        self.calendar_container_1 = ft.Container(
            bgcolor=self.color_teal,
            border_radius=20,
            expand=True,
            padding=20,
            content=ft.Container()
        )

        ################################### PAGINA 4 (CONFIGURACION) ####################################
        self.setting_container_1 = ft.Container(
            bgcolor=self.color_teal,
            border_radius=20,
            expand=True,
            padding=20,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                controls=[self.config_container]
            )
        )

        ################################### PÁGINA 5 (GRÁFICAS) ####################################
        # Los textos que se actualizarán dinámicamente
        self.titulo_grafica_text = ft.Text(
            value="Gráfica del Manómetro",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900
        )
        
        # ¡IMPORTANTE! Este Text mostrará el valor ACTUAL en tiempo real
        self.presion_actual_display = ft.Text(
            value="-- Pa",  # Valor inicial
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREEN_700
        )
        
        # Textos DINÁMICOS para la leyenda de límites
        self.leyenda_superior_text = ft.Text(
            value="Límite superior (-- Pa)",  # Se actualizará dinámicamente
            size=11, 
            color=ft.Colors.RED_700
        )
        self.leyenda_inferior_text = ft.Text(
            value="Límite inferior (-- Pa)",  # Se actualizará dinámicamente
            size=11, 
            color=ft.Colors.GREEN_700
        )
        
        # Gráfica
        self.grafica_chart = ft.LineChart(
            expand=True,
            tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
            border=ft.border.all(1, ft.Colors.GREY_300),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=1, color=ft.Colors.GREY_300, width=1
            ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=1, color=ft.Colors.GREY_300, width=1
            ),
            left_axis=ft.ChartAxis(
                labels_size=40,
                title=ft.Text("Presión (Pa)", size=12)
            ),
            bottom_axis=ft.ChartAxis(
                labels_size=40,
                title=ft.Text("Fecha y Hora", size=12)
            ),
            min_y=70,
            max_y=120,
        )
        
        # Línea de la gráfica principal (SIN curvas)
        self.linea_grafica = ft.LineChartData(
            color=ft.Colors.BLUE_700,
            stroke_width=2,
            curved=False,  # SIN curvas - línea recta
            stroke_cap_round=False,
            # Los puntos se configuran en cada LineChartDataPoint individualmente
        )
        
        # Línea de límite superior (108 Pa)
        self.linea_limite_superior = ft.LineChartData(
            color=ft.Colors.RED_700,
            stroke_width=2,
            curved=False,
            stroke_cap_round=False,
            dash_pattern=[10, 5],  # Línea punteada
        )
        
        # Línea de límite inferior (80 Pa)
        self.linea_limite_inferior = ft.LineChartData(
            color=ft.Colors.GREEN_700,
            stroke_width=2,
            curved=False,
            stroke_cap_round=False,
            dash_pattern=[10, 5],  # Línea punteada
        )
        
        # Lista de historial para gráficas
        self.lista_historial_grafica = ft.ListView(
            expand=True,
            spacing=5,
            padding=10
        )
        
        # Contador de registros
        self.contador_registros = ft.Text(
            "0 registros",
            size=14,
            color=ft.Colors.GREY_600
        )
        
        # Botón de actualizar
        self.btn_actualizar_grafica = ft.IconButton(
            icon=ft.Icons.REFRESH,
            icon_color=ft.Colors.BLUE_600,
            tooltip="Actualizar gráfica",
            on_click=lambda e: self.actualizar_historial_manometro()
        )
        
        self.grafica_container = ft.Container(
            bgcolor=self.color_teal,
            border_radius=20,
            expand=True,
            padding=20,
            content=ft.Column(
                expand=True,
                spacing=20,
                controls=[
                    # CABECERA
                    ft.Container(
                        padding=ft.padding.symmetric(vertical=10, horizontal=15),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=10,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=5,
                            color=ft.Colors.GREY_300,
                        ),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=ft.Colors.BLUE_700,
                                    icon_size=28,
                                    on_click=lambda e: self.change_page_manual(1),
                                    tooltip="Volver a Manómetros"
                                ),
                                self.titulo_grafica_text,
                                self.btn_actualizar_grafica
                            ]
                        )
                    ),
                    
                    # CONTENIDO PRINCIPAL
                    ft.Container(
                        expand=True,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=15,
                        padding=25,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.Colors.GREY_300,
                        ),
                        content=ft.Row(
                            expand=True,
                            spacing=20,
                            controls=[
                                # Panel izquierdo - Grafica
                                ft.Container(
                                    expand=2,  # 2/3 del espacio
                                    padding=20,
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=10,
                                    content=ft.Column(
                                        expand=True,
                                        spacing=10,
                                        controls=[
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    ft.Text("Gráfica de Presión", 
                                                        size=18, weight=ft.FontWeight.BOLD),
                                                    self.contador_registros
                                                ]
                                            ),
                                            
                                            ft.Divider(height=1, color=ft.Colors.GREY_300),
                                            
                                            # Gráfica
                                            ft.Container(
                                                expand=True,
                                                border=ft.border.all(1, ft.Colors.GREY_300),
                                                border_radius=10,
                                                padding=10,
                                                content=self.grafica_chart
                                            ),
                                            
                                            # Info adicional CON LEYENDA DINÁMICA
                                            ft.Container(
                                                padding=10,
                                                bgcolor=ft.Colors.BLUE_50,
                                                border_radius=5,
                                                content=ft.Column(
                                                    spacing=8,
                                                    controls=[
                                                        ft.Row(
                                                            spacing=10,
                                                            controls=[
                                                                ft.Text("Presión actual:", size=14, color=ft.Colors.GREY_600),
                                                                self.presion_actual_display,
                                                            ]
                                                        ),
                                                        # Leyenda de límites DINÁMICA
                                                        ft.Container(
                                                            margin=ft.margin.only(top=5),
                                                            content=ft.Column(
                                                                spacing=3,
                                                                controls=[
                                                                    ft.Text("Límites de referencia:", size=12, color=ft.Colors.GREY_700),
                                                                    ft.Row(
                                                                        spacing=15,
                                                                        controls=[
                                                                            ft.Row([
                                                                                ft.Container(width=15, height=2, 
                                                                                            bgcolor=ft.Colors.RED_700),
                                                                                self.leyenda_superior_text,
                                                                            ]),
                                                                            ft.Row([
                                                                                ft.Container(width=15, height=2, 
                                                                                            bgcolor=ft.Colors.GREEN_700),
                                                                                self.leyenda_inferior_text,
                                                                            ]),
                                                                            ft.Row([
                                                                                ft.Container(width=10, height=10, 
                                                                                            bgcolor=ft.Colors.BLUE_700, 
                                                                                            border_radius=5),
                                                                                ft.Text("Registro", size=11, color=ft.Colors.BLUE_700),
                                                                            ]),
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ]
                                                )
                                            )
                                        ]
                                    )
                                ),
                                # Panel derecho - Historial
                                ft.Container(
                                    expand=1,  # 1/3 del espacio
                                    padding=20,
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=10,
                                    content=ft.Column(
                                        expand=True,
                                        spacing=10,
                                        controls=[
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    ft.Text("Historial de Registros", 
                                                        size=18, weight=ft.FontWeight.BOLD),
                                                ]
                                            ),
                                            # ENCABEZADO DE TABLA
                                            ft.Container(
                                                padding=10,
                                                bgcolor=ft.Colors.BLUE_100,
                                                border_radius=5,
                                                margin=ft.margin.only(bottom=5),
                                                content=ft.Row([
                                                    ft.Container(
                                                        width=80,
                                                        content=ft.Text("Presión", 
                                                                    weight=ft.FontWeight.BOLD,
                                                                    color=ft.Colors.BLUE_800,
                                                                    size=12)
                                                    ),
                                                    ft.Container(
                                                        width=80,
                                                        content=ft.Text("Fecha", 
                                                                    weight=ft.FontWeight.BOLD,
                                                                    color=ft.Colors.BLUE_800,
                                                                    size=12)
                                                    ),
                                                    ft.Container(
                                                        width=60,
                                                        content=ft.Text("Hora", 
                                                                    weight=ft.FontWeight.BOLD,
                                                                    color=ft.Colors.BLUE_800,
                                                                    size=12)
                                                    ),
                                                    ft.Container(
                                                        width=60,
                                                        content=ft.Text("Tipo", 
                                                                    weight=ft.FontWeight.BOLD,
                                                                    color=ft.Colors.BLUE_800,
                                                                    size=12)
                                                    ),
                                                ])
                                            ),
                                            
                                            ft.Divider(height=1, color=ft.Colors.GREY_300),
                                            
                                            # Área de historial
                                            ft.Container(
                                                expand=True,
                                                border=ft.border.all(1, ft.Colors.GREY_300),
                                                border_radius=10,
                                                padding=10,
                                                content=self.lista_historial_grafica
                                            ),
                                            
                                            # Leyenda
                                            ft.Container(
                                                padding=10,
                                                content=ft.Row(
                                                    spacing=15,
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.Row([
                                                            ft.Container(width=12, height=12, 
                                                                    bgcolor=ft.Colors.BLUE_50, 
                                                                    border_radius=6),
                                                            ft.Text("Automático", size=10),
                                                        ]),
                                                        ft.Row([
                                                            ft.Container(width=12, height=12, 
                                                                    bgcolor=ft.Colors.GREEN_50, 
                                                                    border_radius=6),
                                                            ft.Text("Manual", size=10),
                                                        ]),
                                                    ]
                                                )
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )

        # NUEVO: Agregar la página de gráficas a la lista
        self.container_list_1 = [
            self.home_container_1,      # índice 0: UMA
            self.location_container_1,  # índice 1: Manómetros  
            self.calendar_container_1,  # índice 2: Alertas
            self.setting_container_1,   # índice 3: Configuración
            self.grafica_container      # NUEVO índice 4: Gráficas
        ]

        self.container_1 = ft.Container(
            content=self.container_list_1[0], 
            expand=True,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
        )

        # ========== BARRA DE NAVEGACIÓN PROFESIONAL ==========
        # Botones de navegación con diseño profesional
        self.btn_connect = self._crear_boton_navegacion_profesional("UMA", ft.Icons.MONITOR_HEART, 0)
        self.btn_connect2 = self._crear_boton_navegacion_profesional("Manómetros", ft.Icons.SPEED, 1)
        self.btn_connect3 = self._crear_boton_navegacion_profesional("Alertas", ft.Icons.NOTIFICATIONS, 2)
        self.btn_connect4 = self._crear_boton_navegacion_profesional("Configuración", ft.Icons.SETTINGS, 3)

        # Barra lateral de navegación profesional
        self.navigation_container = ft.Container(
            col=2,
            expand=True,
            bgcolor=ft.Colors.WHITE,
            border_radius=0,
            border=ft.border.only(right=ft.border.BorderSide(1, self.color_borde)),
            padding=ft.padding.symmetric(vertical=30, horizontal=20),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color="rgba(39, 245, 180, 0.08)",
                offset=ft.Offset(5, 0)
            ),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                spacing=15,
                controls=[
                    # Logo y nombre
                    ft.Container(
                        padding=ft.padding.only(bottom=30),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                            controls=[
                                ft.Container(
                                    width=60,
                                    height=60,
                                    border_radius=15,
                                    bgcolor=self.color_primario,
                                    alignment=ft.alignment.center,
                                    shadow=ft.BoxShadow(
                                        spread_radius=0,
                                        blur_radius=15,
                                        color="rgba(39, 245, 180, 0.15)",
                                    ),
                                    content=ft.Icon(
                                        ft.Icons.MONITOR_HEART,
                                        color=ft.Colors.WHITE,
                                        size=30
                                    )
                                ),
                                ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=2,
                                    controls=[
                                        ft.Text(
                                            "Sistema de",
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            color=self.color_texto
                                        ),
                                        ft.Text(
                                            "Monitoreo",
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            color=self.color_primario
                                        )
                                    ]
                                )
                            ]
                        )
                    ),
                    
                    ft.Divider(height=20, color=self.color_borde),
                    
                    # Botones de navegación
                    self.btn_connect,
                    self.btn_connect2,
                    self.btn_connect3,
                    self.btn_connect4,
                    
                    ft.Divider(height=30, color=self.color_borde),
                    
                    # Estado del sistema
                    ft.Container(
                        padding=15,
                        bgcolor=f"{self.color_primario}08",
                        border_radius=10,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                            controls=[
                                ft.Row(
                                    spacing=8,
                                    controls=[
                                        ft.Container(
                                            width=10,
                                            height=10,
                                            border_radius=5,
                                            bgcolor=self.color_primario
                                        ),
                                        ft.Text(
                                            "Sistema Activo",
                                            size=12,
                                            weight=ft.FontWeight.W_600,
                                            color=self.color_texto
                                        )
                                    ]
                                ),
                                ft.Text(
                                    datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                                    size=11,
                                    color=self.color_texto_secundario
                                )
                            ]
                        )
                    )
                ]
            )
        )

        # Área principal de contenido
        self.frame_2 = ft.Container(
            col=10,
            alignment=ft.alignment.center,
            bgcolor=self.color_teal,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    self.container_1,
                ]
            )   
        )
        
        # Layout principal
        self.resp_container = ft.ResponsiveRow(
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                self.navigation_container,
                self.frame_2,
            ]
        )

        self.iniciar_home_random()
        
        # Inicializar botón activo
        self.actualizar_colores_botones(0)

    def redondear_entero_desde_6(self, valor):
        """Redondea hacia arriba desde 0.6"""
        parte_entera = int(valor)
        decimal = valor - parte_entera
        return parte_entera + 1 if decimal >= 0.6 else parte_entera
    
    def generar_datos_random(self):
        """Genera datos aleatorios con verificación de alertas"""
        temp_original = random.uniform(15, 35)
        hum_original = random.uniform(30, 90)
        pres1_original = random.uniform(80, 110)
        pres2_original = random.uniform(80, 110)
        pres3_original = random.uniform(80, 110)

        temp = self.redondear_entero_desde_6(temp_original)
        hum = self.redondear_entero_desde_6(hum_original)
        pres1 = self.redondear_entero_desde_6(pres1_original)
        pres2 = self.redondear_entero_desde_6(pres2_original)
        pres3 = self.redondear_entero_desde_6(pres3_original)

        self.datos_tiempo_real = {
            'temperatura': temp,
            'humedad': hum, 
            'presion1': pres1,
            'presion2': pres2,
            'presion3': pres3,
        }

        # Actualizar manómetros
        for key, box in self.blue_boxes.items():
            if hasattr(box, 'actualizar_valor'):
                valor = self.datos_tiempo_real[key]
                box.actualizar_valor(f"{valor} Pa")

        # Verificar alertas - usar el nuevo método
        # if temp > 30:
        #     self.agregar_alerta_y_actualizar(
        #         causa=f"Temperatura CRÍTICA: {temp}°C (supera 30°C)",
        #         pagina="UMA"
        #     )
        
        # if hum > 85:
        #     self.agregar_alerta_y_actualizar(
        #         causa=f"Humedad ALTA: {hum}% (superior a 85%)",
        #         pagina="UMA"
        #     )
        
        # if pres1 > 108:
        #     self.agregar_alerta_y_actualizar(
        #         causa=f"Presión ALTA: {pres1}Pa (supera 108 Pa)",
        #         pagina="UMA"
        #     )
        
        # if pres2 > 108:
        #     self.agregar_alerta_y_actualizar(
        #         causa=f"Presión ALTA: {pres2}Pa (supera 108 Pa)",
        #         pagina="UMA"
        #     )
        
        # if pres3 > 108:
        #     self.agregar_alerta_y_actualizar(
        #         causa=f"Presión ALTA: {pres3}Pa (supera 108 Pa)",
        #         pagina="UMA"
        #     )
        if temp > 38:
            self.agregar_alerta_y_actualizar(
                causa=f"Temperatura CRÍTICA: {temp}°C (supera 30°C)",
                pagina="UMA",
                elemento="Manómetro 09 T",
                valor=f"{pres1} Pa",
                tipo="critica" if temp > 40 else "advertencia"
            )
        
        if hum > 85:
            self.agregar_alerta_y_actualizar(
                causa=f"Humedad ALTA: {hum}% (superior a 85%)",
                pagina="UMA",
                elemento="Manómetro 09 H",
                valor=f"{pres1} Pa",
                tipo="critica" if hum > 90 else "advertencia"
            )

        if pres1 > 108:
            self.agregar_alerta_y_actualizar(
                causa="Presión ALTA (supera 108 Pa)",
                pagina="Manómetros",
                elemento="Manómetro 1",
                valor=f"{pres1} Pa",
                tipo="critica" if pres1 > 110 else "advertencia"
            )

        if pres2 > 108:
            self.agregar_alerta_y_actualizar(
                causa="Presión ALTA (supera 108 Pa)",
                pagina="Manómetros",
                elemento="Manómetro 2",
                valor=f"{pres2} Pa",
                tipo="critica" if pres2 > 110 else "advertencia"
            )

        if pres3 > 108:
            self.agregar_alerta_y_actualizar(
                causa="Presión ALTA (supera 108 Pa)",
                pagina="Manómetros",
                elemento="Manómetro 3",
                valor=f"{pres3} Pa",
                tipo="critica" if pres3 > 110 else "advertencia"
            )
        
        return {"presion1": pres1, "presion2": pres2, "presion3": pres3, "temperatura": temp, "humedad": hum}

    def iniciar_home_random(self):
        """Inicia la generación aleatoria de datos"""
        def loop():
            while True:
                datos = self.generar_datos_random()
                
                def actualizar():
                    # Actualiza los controles que UMA usa
                    self.txt_temp_home.value = f"{datos['temperatura']} °C"
                    self.txt_hum_home.value = f"{datos['humedad']} %"
                    self.txt_pres_home.value = f"{datos['presion1']} Pa"
                    
                    # ¡NUEVO! Actualizar también la página de gráficas si estamos en ella
                    if (hasattr(self, 'manometro_activo') and 
                        hasattr(self, 'presion_actual_display') and
                        self.container_1.content == self.grafica_container):
                        
                        # Obtener el valor directamente como dijiste
                        if "MANOMETRO 1" in self.manometro_activo:
                            self.presion_actual_display.value = f"{self.datos_tiempo_real['presion1']} Pa"
                        elif "MANOMETRO 2" in self.manometro_activo:
                            self.presion_actual_display.value = f"{self.datos_tiempo_real['presion2']} Pa"
                        elif "MANOMETRO 3" in self.manometro_activo:
                            self.presion_actual_display.value = f"{self.datos_tiempo_real['presion3']} Pa"
                    
                    self.page.update()
                
                self.page.run_thread(actualizar)
                time.sleep(2)  # Ya tienes este intervalo
        
        threading.Thread(target=loop, daemon=True).start()

    def change_page_manual(self, index):
        """Cambia entre páginas de la aplicación"""
        self.container_1.content = self.container_list_1[index]
        self.actualizar_colores_botones(index)
        
        # Actualizar estado de la página de Alertas
        if index == 2:  # Si estamos entrando a Alertas
            self.en_pagina_alertas = True
            # Ocultar el badge
            if self.notificacion_badge is not None:
                self.notificacion_badge.visible = False
                try:
                    self.notificacion_badge.update()
                except:
                    pass
        else:  # Si estamos saliendo de Alertas
            self.en_pagina_alertas = False
            # Actualizar el contador para que se muestre si hay alertas
            self.actualizar_contador_alertas()
        
        # Si estamos entrando a la página de gráficas, actualizar datos
        if index == 4 and self.manometro_activo and self.manometro_numero:
            self.page.run_thread(self.actualizar_historial_manometro)
        
        if self.alertas_view is not None:
            if index == 2:  # Alertas está en índice 2
                if hasattr(self.alertas_view, 'entrar_a_pagina'):
                    self.alertas_view.entrar_a_pagina()
            else:
                if hasattr(self.alertas_view, 'salir_de_pagina'):
                    self.alertas_view.salir_de_pagina()

        self.page.update()
    
    def actualizar_colores_botones(self, index_activo):
        """Actualiza los colores y formas de los botones de navegación"""
        botones = [self.btn_connect, self.btn_connect2, self.btn_connect3, self.btn_connect4]
        
        for i, btn in enumerate(botones):
            if i == index_activo:
                # Botón activo: Color primario con fondo
                btn.bgcolor = self.color_primario
                btn.border = ft.border.all(1, self.color_primario)
                
                # Obtener el contenido del botón
                contenido = btn.content
                
                # Si es el botón de Alertas (con Stack)
                if i == 2 and isinstance(contenido, ft.Stack):
                    boton_container = contenido.controls[0]
                    if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
                        row_controls = boton_container.content.controls
                        if len(row_controls) > 1:
                            if hasattr(row_controls[0], 'color'):
                                row_controls[0].color = ft.Colors.WHITE
                            if hasattr(row_controls[1], 'color'):
                                row_controls[1].color = ft.Colors.WHITE
                else:
                    # Para botones normales
                    if isinstance(contenido, ft.Row):
                        row_controls = contenido.controls
                        if len(row_controls) > 1:
                            if hasattr(row_controls[0], 'color'):
                                row_controls[0].color = ft.Colors.WHITE
                            if hasattr(row_controls[1], 'color'):
                                row_controls[1].color = ft.Colors.WHITE
                btn.scale = ft.Scale(1.0)
            else:
                # Botones inactivos: Blanco con borde gris
                btn.bgcolor = ft.Colors.WHITE
                btn.border = ft.border.all(1, self.color_borde)
                
                # Obtener el contenido del botón
                contenido = btn.content
                
                # Si es el botón de Alertas (con Stack)
                if i == 2 and isinstance(contenido, ft.Stack):
                    boton_container = contenido.controls[0]
                    if hasattr(boton_container, 'content') and isinstance(boton_container.content, ft.Row):
                        row_controls = boton_container.content.controls
                        if len(row_controls) > 1:
                            if hasattr(row_controls[0], 'color'):
                                row_controls[0].color = self.color_texto_secundario
                            if hasattr(row_controls[1], 'color'):
                                row_controls[1].color = self.color_texto
                else:
                    # Para botones normales
                    if isinstance(contenido, ft.Row):
                        row_controls = contenido.controls
                        if len(row_controls) > 1:
                            if hasattr(row_controls[0], 'color'):
                                row_controls[0].color = self.color_texto_secundario
                            if hasattr(row_controls[1], 'color'):
                                row_controls[1].color = self.color_texto
                btn.scale = ft.Scale(1.0)
        
        # Actualizar todos los botones de forma segura
        for btn in botones:
            try:
                btn.update()
            except:
                pass

    def abrir_pagina_grafica(self, titulo_manometro):
        """Abre la página de gráficas para un manómetro específico"""
        print(f"Abriendo gráfica para: {titulo_manometro}")
        
        # 1. Guardar referencia al manómetro activo
        self.manometro_activo = titulo_manometro
        
        # 2. Obtener datos del manómetro específico
        if "MANOMETRO 1" in titulo_manometro:
            self.manometro_numero = 1
            datos = self.datos_tiempo_real['presion1']
        elif "MANOMETRO 2" in titulo_manometro:
            self.manometro_numero = 2
            datos = self.datos_tiempo_real['presion2']
        elif "MANOMETRO 3" in titulo_manometro:
            self.manometro_numero = 3
            datos = self.datos_tiempo_real['presion3']
        else:
            self.manometro_numero = None
            datos = 0
        
        # 3. Actualizar el título de la página
        self.titulo_grafica_text.value = f"Gráfica: {titulo_manometro}"
        
        # 4. Actualizar el valor inicial en el display
        self.presion_actual_display.value = f"{datos} Pa"
        
        # 5. Cambiar a la página de gráficas (índice 4)
        self.change_page_manual(4)
        
        # 6. Actualizar historial y gráfica
        self.page.run_thread(self.actualizar_historial_manometro)
        
        # 7. Imprimir confirmación
        print(f"✓ Página de gráficas abierta para {titulo_manometro}")
        print(f"  Presión actual: {datos} Pa")
        print(f"  Número de manómetro: {self.manometro_numero}")

    def crear_punto_grafica(self, x, y):
        """Crea un punto de datos para la gráfica CON PUNTO VISIBLE"""
        return ft.LineChartDataPoint(
            x,
            y,
            selected_below_line=ft.ChartPointLine(
                width=0.5, color=ft.Colors.GREY_400, dash_pattern=[2, 4]
            ),
            selected_point=ft.ChartCirclePoint(
                stroke_width=2, 
                color=ft.Colors.BLUE_700,
                radius=6,  # Punto más grande
                # color_solid=ft.Colors.BLUE_700,  # Color sólido del punto
            ),
            # show=True,  # Asegurar que el punto se muestre
        )

    def actualizar_historial_manometro(self, e=None):
        """Actualiza la gráfica y la lista de historial para el manómetro activo"""
        if not self.manometro_activo or not self.manometro_numero:
            print("No hay manómetro activo")
            return
        
        print(f"Actualizando historial para manómetro {self.manometro_numero}")
        
        # DEFINIR LÍMITES DIFERENTES PARA CADA MANÓMETRO
        if self.manometro_numero == 1:
            limite_superior = 108  # Límite para manómetro 1
            limite_inferior = 80   # Límite para manómetro 1
        elif self.manometro_numero == 2:
            limite_superior = 105  # Límite diferente para manómetro 2
            limite_inferior = 82   # Límite diferente para manómetro 2
        elif self.manometro_numero == 3:
            limite_superior = 110  # Límite diferente para manómetro 3
            limite_inferior = 78   # Límite diferente para manómetro 3
        else:
            limite_superior = 108
            limite_inferior = 80
        
        # ACTUALIZAR LEYENDA CON LOS LÍMITES CORRECTOS
        self.actualizar_leyenda_limites(limite_superior, limite_inferior)
        
        # Obtener registros del manómetro desde el historial principal
        registros = self.reloj_global.obtener_registros_por_manometro(
            self.manometro_numero, 
            limite=20
        )
        
        # Actualizar contador
        self.contador_registros.value = f"{len(registros)} registros"
        
        # Limpiar gráfica actual
        puntos_grafica = []
        puntos_limite_superior = []
        puntos_limite_inferior = []
        
        if registros:
            # Crear etiquetas para el eje X (fechas)
            etiquetas_x = []
            
            # Agregar puntos a la gráfica (X = timestamp, Y = presión)
            for i, registro in enumerate(registros):
                # Usar timestamp como X para espaciar correctamente
                timestamp = registro['fecha_hora'].timestamp()
                
                # Punto de datos real CON PUNTO VISIBLE
                punto = self.crear_punto_grafica(timestamp, registro['presion'])
                puntos_grafica.append(punto)
                
                # Punto para línea de límite superior (con límite personalizado)
                punto_superior = ft.LineChartDataPoint(timestamp, limite_superior)
                puntos_limite_superior.append(punto_superior)
                
                # Punto para línea de límite inferior (con límite personalizado)
                punto_inferior = ft.LineChartDataPoint(timestamp, limite_inferior)
                puntos_limite_inferior.append(punto_inferior)
                
                # Crear etiqueta para el eje X (fecha corta)
                fecha_corta = registro['fecha_hora'].strftime("%d/%m\n%H:%M")
                etiquetas_x.append(ft.ChartAxisLabel(
                    value=timestamp,
                    label=ft.Text(fecha_corta, size=10)
                ))
            
            # Configurar eje X con las etiquetas de fecha
            self.grafica_chart.bottom_axis = ft.ChartAxis(
                labels=etiquetas_x,
                labels_size=35,
                labels_interval=1 if len(etiquetas_x) <= 10 else 2,
                title=ft.Text("Fecha y Hora", size=12)
            )
            
            # Configurar rango Y dinámico considerando los límites personalizados
            presiones = [r['presion'] for r in registros]
            min_presion = min(presiones) if presiones else limite_inferior
            max_presion = max(presiones) if presiones else limite_superior
            
            # Agregar margen para que se vean bien los límites
            self.grafica_chart.min_y = min(limite_inferior - 10, min_presion - 10)
            self.grafica_chart.max_y = max(limite_superior + 10, max_presion + 10)
            
            # Configurar eje Y
            self.grafica_chart.left_axis = ft.ChartAxis(
                labels_size=40,
                title=ft.Text("Presión (Pa)", size=12)
            )
            
            # Actualizar línea de la gráfica principal
            self.linea_grafica.data_points = puntos_grafica
            self.linea_grafica.curved = False
            
            # Actualizar línea de límite superior
            self.linea_limite_superior.data_points = puntos_limite_superior
            self.linea_limite_superior.curved = False
            
            # Actualizar línea de límite inferior
            self.linea_limite_inferior.data_points = puntos_limite_inferior
            self.linea_limite_inferior.curved = False
            
            # Agregar todas las líneas a la gráfica
            self.grafica_chart.data_series = [
                self.linea_grafica,
                self.linea_limite_superior,
                self.linea_limite_inferior
            ]
        else:
            # Si no hay registros, solo mostrar líneas de límite
            self.grafica_chart.data_series = []
        
        # Limpiar lista actual
        self.lista_historial_grafica.controls.clear()
        
        # Agregar registros a la lista (más reciente primero)
        for registro in reversed(registros):  # Invertir para mostrar más reciente arriba
            # Determinar color según tipo
            if "automatico" in registro['tipo']:
                color_fondo = ft.Colors.BLUE_50
                icono = ft.Icons.AUTORENEW
                color_icono = ft.Colors.BLUE_600
            elif "manual" in registro['tipo']:
                color_fondo = ft.Colors.GREEN_50
                icono = ft.Icons.TOUCH_APP
                color_icono = ft.Colors.GREEN_600
            else:
                color_fondo = ft.Colors.GREY_50
                icono = ft.Icons.INFO
                color_icono = ft.Colors.GREY_600
            
            # Determinar si está por encima del límite (usando límite personalizado)
            sobre_limite = registro['presion'] > limite_superior
            
            # Crear fila para la tabla
            fila = ft.Container(
                padding=10,
                bgcolor=ft.Colors.RED_50 if sobre_limite else color_fondo,
                border_radius=5,
                margin=ft.margin.only(bottom=5),
                content=ft.Row([
                    # Presión
                    ft.Container(
                        width=80,
                        content=ft.Text(
                            f"{registro['presion']} Pa",
                            size=12,
                            color=ft.Colors.RED_700 if sobre_limite else ft.Colors.BLUE_700,
                            weight=ft.FontWeight.BOLD
                        )
                    ),
                    # Fecha
                    ft.Container(
                        width=80,
                        content=ft.Text(
                            registro['fecha'],
                            size=12,
                            color=ft.Colors.GREY_700
                        )
                    ),
                    # Hora
                    ft.Container(
                        width=60,
                        content=ft.Text(
                            registro['hora'],
                            size=12,
                            color=ft.Colors.GREY_700
                        )
                    ),
                    # Tipo con icono
                    ft.Container(
                        width=60,
                        content=ft.Row([
                            ft.Icon(icono, size=14, color=color_icono),
                            ft.Text(
                                "Auto" if "automatico" in registro['tipo'] else "Manual",
                                size=10,
                                color=color_icono
                            )
                        ], spacing=5)
                    ),
                ])
            )
            
            self.lista_historial_grafica.controls.append(fila)
        
        # Si no hay registros, mostrar mensaje
        if not registros:
            self.lista_historial_grafica.controls.append(
                ft.Container(
                    padding=20,
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            ft.Icon(ft.Icons.HISTORY, size=48, color=ft.Colors.GREY_400),
                            ft.Text(
                                "No hay registros históricos",
                                size=14,
                                color=ft.Colors.GREY_500
                            )
                        ]
                    )
                )
            )
        
        # Actualizar todos los componentes
        try:
            self.grafica_chart.update()
            self.lista_historial_grafica.update()
            self.contador_registros.update()
            self.presion_actual_display.update()
        except Exception as e:
            print(f"Error actualizando componentes: {e}")

    def actualizar_leyenda_limites(self, limite_superior, limite_inferior):
        """Actualiza la leyenda con los límites específicos del manómetro"""
        # Actualizar los textos de la leyenda
        self.leyenda_superior_text.value = f"Límite superior ({limite_superior} Pa)"
        self.leyenda_inferior_text.value = f"Límite inferior ({limite_inferior} Pa)"
        
        # Actualizar los componentes
        try:
            self.leyenda_superior_text.update()
            self.leyenda_inferior_text.update()
        except Exception as e:
            print(f"Error actualizando leyenda: {e}")
        
        print(f"Límites actualizados: Superior={limite_superior} Pa, Inferior={limite_inferior} Pa")

    def will_unmount(self):
        """Detener el reloj global al cerrar la app"""
        self.reloj_global.detener()


def main(page: ft.Page):
    page.title = "Sistema de Monitoreo Inteligente"
    page.window.width = 1400
    page.window.height = 750
    page.window.resizable = True
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.bgcolor = ft.Colors.WHITE
    page.padding = 0

    ui = UI(page)
    page.add(ui)

if __name__ == "__main__":
    ft.app(target=main)