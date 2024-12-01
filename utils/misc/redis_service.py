from redis import Redis


class RedisService:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self._redis = Redis(host=host, port=port, db=db, decode_responses=True)

    def set_products(self, lang: str, products: dict):
        self._redis.hset(name=f'product_{lang}', mapping=products)

    def get_products(self, lang: str):
        return self._redis.hgetall(name=f'product_{lang}')

    def get_product_pk(self, lang: str, p_name: str):
        res = self._redis.hgetall(name=f'product_{lang}')
        return int(res.get(p_name))

    def get_all_products(self):
        res_uz = self._redis.hgetall(name='product_uz')
        res_ru = self._redis.hgetall(name='product_ru')
        res_uz.update(res_ru)
        return res_uz

    def set_products_price(self, data: dict):
        self._redis.hset(name=f"products_price", mapping=data)

    def get_product_price(self, p_name: str):
        result = self._redis.hgetall(name=f"products_price")
        return result.get(p_name)

    def get_all_products_price(self):
        return self._redis.hgetall(name='products_price')

    def set_user_basket(self, pk, data: dict):
        old_data = self._redis.hgetall(name=str(pk))
        old_data.update(data)
        self._redis.hset(name=str(pk), mapping=data)

    def get_user_basket(self, pk):
        return self._redis.hgetall(name=str(pk))

    def delete_user_basket(self, pk, product_name=None, _all=False):
        if _all:
            self._redis.delete(str(pk))
            return
        basket = self._redis.hgetall(name=str(pk))
        new_data = dict(basket.copy())
        new_data.pop(product_name)
        self._redis.delete(str(pk))
        if new_data:
            self._redis.hset(name=str(pk), mapping=new_data)

    def get_user_location(self, user_id):
        return {
            'latitude': self._redis.hget(name=str(user_id), key='latitude'),
            'longitude': self._redis.hget(name=str(user_id), key='longitude')
        }

    def set_user_comment(self, user_id, comment: str) -> int:
        return int(self._redis.hset(name=str(user_id), key='comment', value=comment))

    def get_user_comment(self, user_id) -> int:
        return self._redis.hset(name=str(user_id), key='comment')

    def get_user_data(self, user_id) -> dict:
        return self._redis.hgetall(name=str(user_id))

    def delete_user_data(self, user_id):
        self._redis.hdel(
            str(user_id), *['order_pk', 'fullname', 'phone_number', 'latitude', 'longitude', 'comment'])

    def flush_all(self) -> None:
        return self._redis.flushall()
