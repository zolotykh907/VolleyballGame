# VolleyballGame

![Логотип](images/screenshot.png)


<details open>
  <summary>
    <h2>
      <p>
        1. Описание
      </p>
    </h2>
  </summary> 
Волейбол на Python для двоих игроков, против ПК.
- Один игрок - нападающий, другой связующий
- Из игровых действий - прием, пас, удар, подача
- Возможность совершать два варианта нападающего удара:
    - "Обычный", связующий стоит, пас высокий
    - "Взлет", связующий дает невысокий пас в прыжке
- Подача пока выполняется только со стороны компьютера
- Обработка большинства игровых ситуаций:
    - Касание сетки
    - Мяч попал в поле или аут
    - Превышение лимита касаний на одну команду
    - Удар в сетку

# Запуск
- Запустить main.exe

Для двух следующих способов нужно установить зависимости из src/requirements.txt:

```
pip install -r src/requirements.txt
```

Далее:
- Перейти в папку src и запустить в компиляторе main.py
- Перейти в папку src и запустить через командную строку main.py

```
cd src
python main.py
```

# Краткое описание файлов

## main.py
В main.py прописан основной цикл работы программы, а так же функции для вывода некоторых элементов на экран.