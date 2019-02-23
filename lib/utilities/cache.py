"""
Copyright 2019 Glen Harmon



"""

import os
import datetime
import functools
import json

import sublime


class cache:

    @classmethod
    def file(cls, path, expire_minutes=240, encoding='utf-8', is_class_method=False):
        """
            The is_class_method flag will strip the first argument 
        """

        path = os.path.sep.join([sublime.packages_path(), path])
        directory = os.path.sep.join(path.split(os.path.sep)[:-1])

        if not os.path.exists(directory):
            try:
                os.mkdir(directory)
            except FileExistsError:
                pass

        loaded_cache = dict()
        if os.path.isfile(path):
            with open(path, mode='r', encoding=encoding) as f:
                loaded_cache = json.loads(f.read())


        def decorator(function):

            @functools.wraps(function)
            def wrapper(*args, **kwargs):


                if is_class_method:
                    cache_key = json.dumps((args[1:], kwargs), ensure_ascii=False, sort_keys=True)
                else:
                    cache_key = json.dumps((args, kwargs), ensure_ascii=False, sort_keys=True)

                if cache_key in loaded_cache:
                    expire, result = loaded_cache[cache_key]
                    expire = datetime.datetime.strptime(expire, '%Y-%m-%d %H:%M:%S')
                    if (expire - datetime.datetime.now()).total_seconds() > 0:
                        return result
                    loaded_cache.pop(cache_key)

                result = function(*args, **kwargs)

                expire = datetime.datetime.now().replace(second=0, microsecond=0) + datetime.timedelta(minutes=expire_minutes)

                cache = (str(expire), result)

                loaded_cache[cache_key] = cache

                with open(path, mode='w', encoding=encoding) as f:
                    json.dump(
                        loaded_cache,
                        f,
                        sort_keys=True,
                        ensure_ascii=False,
                    )

                return result
            return wrapper
        return decorator

    @classmethod
    def file_method(cls, path, expire_minutes=240, encoding='utf-8'):
        """
            Caches a class method
        """
        return cls.file(path, expire_minutes=expire_minutes, encoding=encoding, is_class_method=True)
