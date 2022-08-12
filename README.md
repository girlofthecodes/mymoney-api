# API creada con con Django Rest Framework
Esta API fue desarrollada para que el usuario pueda llevar un control mas exacto de sus finanzas, donde podra realizar sus 
cuentas, etiquetas, gastos, ingresos, metas, ahorros y un balance general, pero el usuario debe tener en cuenta que para 
poder hacer uso de estos recursos mencionados, debera registrarse en la aplicación, algunas otras funcionalidades que tiene 
la api relacionada al usuario es el registro de usuario, inicio de sesión, reseteo de contraseña, cambio de contraseña, perfil 
de usuario y logout. 
A continuación se explicara brevemente como el usuario puede hacer uso de cada funcionalidad. 

	1. Registro de usuario: 
   	El cual pedira datos obligatorios como: username, email y password. 
		
		{
		 “username”: “Adahack”,
		 “email”: “weisseujeicrefe-2059@yopmail.com”,
		 “password”: “Ada_hack@121”
		}
		
	2. Inicio de Sesión: 
	Una vez el usuario se haya registrado, se enviara el correo de verificación de email, por lo cual una vez se verifique, 
	podrá tener acceso ingresando su email y password.
	
		{
		 “email”: “weisseujeicrefe-2059@yopmail.com”,
		 “password”: “Ada_hack@121”
		}
		
	3. Reseteo de contraseña: 
	El inicio de sesión cuenta con tres intentos por si no recuerda el usuario la contraseña, de pasar los tres intentos, 
	la cuenta se bloqueara y debera de resetear la contraseña para la recuperación de esta. Debera ingresar su contraseña
	para que le llegue un email en el cual traera un token, el cual debera ingresarse para que permita la autenticación y 
	pueda cambiar la contraseña perfectamente, los datos que pedira son email, password, iudb64 y un token.
	
		{
		 “email”: “weisseujeicrefe-2059@yopmail.com”,
		}
		
		{
		 “password”: “Ada_hack@121”, 
		 "uidb64":Ng, 
		 "token":"b9ychv-7a303c3fe383047d8b4bbb389d92ec66"
		}
		
	4. Cambio de contraseña: 
	Si la contraseña actual que tienes no es de agrado del usuario, o por algun motivo, quiere hacer el cambio, tendra la 
	opción de hacerlo siempre y cuando este autenticado, en donde debera ingresar su password actual, nuevo password y 
	confirmación del nuevo password. 
	
		{
		 "current_password": “Ada_hack@121”, 
		 "new_password":"A@jdn345",
		 "confirm_password":"A@jdn345"
		}
		
	5. Perfil de Usuario: 
	El usuario podra crear un perfil de usuario en el cual debera de ingresar datos como primer y segundo nombre, primer y 
	segundo apellido, fecha de nacimiento, lugar de nacimiento, lugar y pais de residencia. Cuenta con la función de que al 
	ingresar la fecha de nacimiento se calculara automaticamente la edad.
  
		{
		 "first_name":"Juan",
		 "middle_name":"Daniel",
		 "first_surname":"Perez",
		 "second_surname":"Hernandez",
		 "birth_date":"1999-04-04",
		 "place_of_birth":"mexico",
		 "residence_place":"mexico",
		 "residence_country":"mexico"
   		}
      
    6. Cuentas: 
    El usuario podra registrar las cuentas bancarias en las que desee llevar un orden mas especifico de sus finanzas, asi 
    como gastos e ingresos. 
    
            {
              "account_name":"Ingresos", 
              "account_type":"Nómina", 
              "account_number":"1234567890123456",
              "current_balance":"3000.00",
              "due_date":"2022-07-21"
            }
            
    7. Etiquetas: 
    El usuario podra registrar etiquetas-concepto, los cuales se relacionaran ya sea con un gasto y/o ingreso, lo cual
    permitira que el usuario tenga un mayor control en sus finanzas. 
    
            {
              "label_name":"Renta",
              "label_type":"Ingreso", 
              "label_class":"Fijo",
              "label_color":"Verde",
              "label_description":"Alquiler de la casa en Chiapas"
            }
            
    8. Gastos: 
    El usuario podra registrar cada uno de los gastos que tenga, y podra ser relacionados con una cuenta y una etiqueta,
    recalcando que el gsto se le ira restando a la cuenta a la que se asocie para tener un mejor control del total de la 
    cuenta. 
    
            {
              "account":"14",
              "label":"10",
              "expense_description":"Compra de ropa para nuevo ciclo escolar",
              "expense_data":"2022-07-25",
              "expense_amount":"900.00"
             }
             
    9. Ingresos: 
    El usuario podra registrar cada uno de los ingresos que tenga, donde podrá relacionar una cuenta y una etiqueta, 
    recalcando que el ingreso se le ira sumando a la cuenta a la que se asocie para tener un mejor control del total de la
    cuenta. 
            {
              "account":"15",
              "label":"11",
              "income_date":"2022-07-02",
              "income_amount":"2500.00",
              "income_description":"Pago de renta"
            }
    
    10. Meta: 
    El usuario podra registrar una meta de ahorro en un periodo de tiempo, este le arrojara un aproximado de cuanto dinero
    tendra al final del periodo. 
    
            {
              "goal_concept":"Viaje",
              "start_date":"2022-07-07",
              "due_date":"2022-10-07",
              "goal_amount":"500.00",
              "goal_period":"Semanal",
              "goal_color":"Verde"
            }
    
    11. Ahorro: 
    El usuario podra ir registrando los ahorros que ira teniendo para asi lograr la meta al cual esta relacionado ese ahorro.
          
            {
              "goal":"4",
              "saving_list":"Viaje", 
              "saving_date": "2022-07-21",
              "saving_amount":"500.00",
              "saving_concept":"Ahorro #3 para el viaje"
            }
            
    12. Balance general: 
    El usuario para un mayor control, podra tener un balance general de sus gastos, ingresos y ahorros, los cuales se podrán 
    filtrar por año, mes y día, y este le dara la suma del filtro que obtuvo. 
            {
            "expense": [
                  {
                      "id": 3,
                      "user": {
                          "id": 6,
                          "email": "butterlfly.atlantis@gmail.com"
                      },
                      "account": {
                          "id": 14,
                          "account_name": "Liverpool"
                      },
                      "label": {
                          "id": 10,
                          "label_name": "Ropa"
                      },
                      "expense_description": "Compra de ropa para nuevo ciclo escolar",
                      "expense_date": "2022-08-10",
                      "expense_amount": "900.00"
                  },
                  {
                      "id": 4,
                      "user": {
                          "id": 6,
                          "email": "butterlfly.atlantis@gmail.com"
                      },
                      "account": {
                          "id": 14,
                          "account_name": "Liverpool"
                      },
                      "label": {
                          "id": 10,
                          "label_name": "Ropa"
                      },
                      "expense_description": "Compra de ropa para nuevo ciclo escolar",
                      "expense_date": "2022-08-10",
                      "expense_amount": "900.00"
                  }
              ],
              "income": [
                  {
                      "id": 7,
                      "user": {
                          "id": 6,
                          "email": "butterlfly.atlantis@gmail.com"
                      },
                      "account": {
                          "id": 15,
                          "account_name": "Ingresos"
                      },
                      "label": {
                          "id": 11,
                          "label_name": "Renta"
                      },
                      "income_date": "2022-08-10",
                      "income_amount": "3000.00",
                      "income_description": "Pago de renta"
                  }
              ],
              "saving": [
                  {
                      "id": 6,
                      "user": {
                          "id": 6,
                          "email": "butterlfly.atlantis@gmail.com"
                      },
                      "goal": {
                          "id": 4,
                          "goal_concept": "Viaje"
                      },
                      "saving_list": "Viaje",
                      "saving_date": "2022-07-07",
                      "saving_amount": "500.00",
                      "saving_concept": "Ahorro #1 para el viaje"
                  },
                  {
                      "id": 7,
                      "user": {
                          "id": 6,
                          "email": "butterlfly.atlantis@gmail.com"
                      },
                      "goal": {
                          "id": 4,
                          "goal_concept": "Viaje"
                      },
                      "saving_list": "Viaje",
                      "saving_date": "2022-07-14",
                      "saving_amount": "500.00",
                      "saving_concept": "Ahorro #2 para el viaje"
                  },
                  {
                      "id": 8,
                      "user": {
                          "id": 6,
                          "email": "butterlfly.atlantis@gmail.com"
                      },
                      "goal": {
                          "id": 4,
                          "goal_concept": "Viaje"
                      },
                      "saving_list": "Viaje",
                      "saving_date": "2022-07-21",
                      "saving_amount": "500.00",
                      "saving_concept": "Ahorro #3 para el viaje"
                  }
              ],
              "total_expense": 1800.0,
              "total_income": 3000.0,
              "total_saving": 1500.0
             }
    
   
