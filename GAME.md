#   kb:game
##  демо гомоиконичной игровой среды
### используется метод EDS: исполняемые структуры данных

(c) Dmitry Ponyatov <<dponyatov@gmail.com>> CC BY-NC-ND 

https://www.youtube.com/watch?v=CoiOKpxsTUI&list=PLTteFr-DCrkQJm-QKnzQz-NyRTWzMse22&index=6

Есть планы продолжать серию?

могу поделиться методикой по написанию своего скриптового движка, если сам
Python оказывается слишком многословным, и хочется какой-то язык специально
заточенный под игру (в качестве иллюстрации, как реализуются интерпретаторы)

так то обычно игры пишут на языках с компиляцией, и там как раз полезно
отделять движок от логики (причем код игры может даже сам себя на ходу
частично переписывать)

есть совсем упоротая штука -- метод **EDS: исполняемые структуры данных** (c),
софт пишется не целиком на каком-то языке программирования типа Python,
только небольшой интерпретирующий движок + построение структур данных которые
могут менять сами себя (исполняемые списки как в Лиспе, атрибутные объектные
графы, параллельные очереди сообщений,...)

там просто возможности безграничные, первое что в голову пришло -- можно
реализовать изменение поведения игры непредусмотренного авторами, если игроки
некоторыми действиями могут менять структуру уровней
