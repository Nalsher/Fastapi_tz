Endpoints:
-/courier/ - POST(метод post который принимает данные с пользователького request'а и сохраняет их в бд) GET(метод get который фетчит все модели таблицы courier)
-/courier/{id} - GET(методом get_by_id мы фетчим сначала имя курьера,затем is_active проверяет есть у курьера активные заказы
                    затем две функции avg_day_ord и avg_time_ord просматривают выполненые заказы курьера и,затем возвращается ответ)
-/order/ - POST(метод post получает данные с пользовательского request'а и сохраняет их в бд)
-/order/{id} - POST(Переводит заказ из orders в orders_done в таблице courier тем самым обозначая что заказ у курьера не активен а был выполнен,
                    также меняет is_active в таблице orders с True на False ) GET(Фетчит с бд информацию о заказе)