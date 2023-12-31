# Содержание
- [Суть проекта](#cуть)
- [Пример использования](#Пример)
- [Как работает?](#Как-работает?)
- [Проблемы](#Проблемы)
- [Установка](#Установка)
# Суть:
___dota2protracker.com___ - сайт, который отслеживает игры про игроков. Информация и статистика о играх на этом сайте хранятся 8 дней (это обусловлено тем, что в самой доте скачать реплей можно только за 8 дней после того, как был сыгран матч). Но хочется иметь статистику и данные о матчах за более продолжительный срок, а также иметь возможность посмотреть матчапы. 

___Матчапы___ - это определенный состав (выбранных нами) героев в одной команде, которые сражаются против определенных героев другой команды. Лично для меня это представляет огромную ценность в обучении игре. [Пример использования](#Пример) 
# Пример 
__Я сыграл игру на своем рейтинге, играя на герое Huskar. Против меня на линии стоял герой Lina. И я проиграл эту игру.__

Пользуясь своим проектом, я могу посмотреть отфильтрованные игры Huskar vs Lina (которые будут храниться в бд) и посмотреть информацию о том, как играли такой же матчап лучшие игроки мира. 
![Поиск матчапа](https://github.com/gomunkul343/dota2protracker_checker/blob/main/src/3.png)

## Результат:
![Результат поиска](https://github.com/gomunkul343/dota2protracker_checker/blob/main/src/2.png)
Чтобы посмотреть новый матчап, нужно нажать на кнопку Find Matchup.


P.S.: 
Полезность проекта увеличивается с количеством времени его работы, т.к. дотабафф ведет политику против парсинга [(подробнее...)](https://www.dotabuff.com/robots.txt). Поэтому имеем ограничение на количество запросов с одного айпи и браузера и поэтому нельзя просто собрать все матчи за последние 8 дней с dota2protracker сразу, и спарсить информацию о матчах, добавив их в БД.

_И в идеале конечно, сделать так, чтобы на сервер также загружались реплеи из самой доты, но тогда нужно задействовать dota api - это очень сложно)_
# Как-работает?
 - Парсер собирает dotabuff ссылки на последние игры, сыгранные про игроками. 
![Парсинг ссылок](https://github.com/gomunkul343/dota2protracker_checker/blob/main/src/1.png)
(Filter mathes, фильтрует только по игрокам, но не по героям)

 - После чего из полученных ссылок парсит каждый матч на дотабаффе.

- Далее добавляет информацию о матчах в БД, проверяя каждый матч на уникальность. После чего мы можем увидеть новые игры.
`(для учебного примера я собирал только базовую информацию: о героях, о стороне, которая победила, сам replay_id, чтобы в доте найти матч, а также саму ссылку на дотабафф, чтобы можно было перейти и посмотреть подробную информацию о матче. Но в целом, загрузив страницу матча на дотабаффе, оттуда можно вытащить какую душе угодно информацию о матче и добавить в БД, дело только во время затратности.)
`
- Парсер работает с перерывом каждые 1-1.5 часа, чтобы недавние матчи обновились и не был получен бан на дотабаффе
# Проблемы
### 1
За слишком частые запросы, Вас могут забанить примерно на сутки.

`
Причина этого заключается в том, что если бы этого ограничения не существовало, то такие люди как я могли бы создать бд с информацией о матчах всех игроков и перед игрой, можно было узнать - на каких героях играют игроки, их winrate, кого брать против, чтобы победить и т.п. 
`

Во время разработки, я очень часто видел retry later =(. Но я постарался настроить парсер так, чтобы он не превышал количество запросов, и собирал информацию о всех последних матчах c dota2protracker. Но вероятность отлететь в бан в нагруженные дни все равно может быть, поэтому на запасной план существует парсер, работающий через selenium. (В app.py, написано как его включить)
### 2
Была проблема, над которой я очень долго думал - как запустить парсер вместе с приложением flask. Но решение оказалось буквально в 5 строчках кода. Спасибо, multiprocessing, за то, что он существует.
### 3
Дотабафф постоянно устраивает подлости, например: меняет название героев в теге с "title" на "oldtitle", из-за чего необходимо проверять, правильно ли была собрана информация.
# Установка
`git clone https://github.com/gomunkul343/dota2protracker_checker.git`

`cd dota2protracker_checker`

`git checkout docker-compose`

`sudo ./build.sh`
