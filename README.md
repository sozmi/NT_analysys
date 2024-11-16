<h1>Решение задач классификации</h1>
<h2>Необходимое окружение и библиотеки</h2>
<p>Версия python - 3.9</p>
<p>Для корректной работы программы необходимы следующие библиотеки:</p>
https://github.com/sozmi/NT_analysys/blob/b8d97373a9e44c7f5ac80eeda1e9335fd6e64b0e/NT_analysis/requirements.txt#L1-L12
<h2>Тестирование</h2>
<p>Работоспособность программы проверялось в ОС - Windows 11.</p>
<p>Также было написано несколько юнит-тестов для проверки действий базового функционала.</p>
<p>Тестирование проводилось при помощи библиотеки unittest. Сами тесты лежат в папке  <a href="https://github.com/sozmi/NT_analysys/tree/master/NT_analysis/tests">tests</a></p>

<h1>Интерфейс и порядок работы</h2>

<h2>Функционал</h2>
<p>Данное приложение позволяет скачивать фотографии при помощи парсинга Яндекс Картинок по запросам из конфигурационного файла, масштабировать их, просматривать, сохранять датасет определённым образом, а также изучать параметры фотоснимков.</p>
<h2>Файл настроек</h2>
В файле настроек можно изменять следующие параметры:
<ul>
  <li>
    В секции изображений(images) можно указать итоговый размер картинок, можно ли скачивать уже сжатые изображения(аватары) или необходимо загрузить оригиналы
    https://github.com/sozmi/NT_analysys/blob/b8d97373a9e44c7f5ac80eeda1e9335fd6e64b0e/NT_analysis/config.xml#L2
  </li>
  <li>
    В секции запросов(queries) указываются запросы по которым нужно скачать изображения. Параметр need-update="True" отвечает за необходимость проверки на достаточность изображений.
     https://github.com/sozmi/NT_analysys/blob/b8d97373a9e44c7f5ac80eeda1e9335fd6e64b0e/NT_analysis/config.xml#L3-L6
  </li>
   <li>
    В секции настройки библиотеки request указываются параметры, которые можно использовать для подключения к Яндекс Картинкам.
    https://github.com/sozmi/NT_analysys/blob/b8d97373a9e44c7f5ac80eeda1e9335fd6e64b0e/NT_analysis/config.xml#L8-L15
  </li>
  <li>
    В секции путей указываются папки, куда будет сохраняться информация, необходимая для работы приложения
    https://github.com/sozmi/NT_analysys/blob/b8d97373a9e44c7f5ac80eeda1e9335fd6e64b0e/NT_analysis/config.xml#L17-L22
  </li>
</ul>

<h2>Руководство пользователя</h2>
<p>Внешний вид приложения:</p>
<img src="https://github.com/user-attachments/assets/536e3f26-c207-4621-91ec-4b139a8f0434" alt="Image" width="400" height="400">
<ol>
  <li>В левом верхнем углу выберите нужный датасет. Если датасетов нет - загрузите его через кнопку "Загрузить"</li>
  <li>Если пользователь хочет получить копию датасета для импорта в другой формат - ему следует нажать кнопку "Создать датасет(случайная нумерация)" "Создать датасет(по тэгам)"</li>
  <li>Чтобы переключаться между изображениями выберите категорию изображения внизу, в центре под картинкой. Далее перемещайтесь по фотографиям кнопками "Следующее изображение" или "Предыдущее изображение"</li>
  <li>Чтобы получить статистику по изображениям, нажмите "Статистика"</li>
  <li>Чтобы получить информацию по пикселям в изображениях, нажмите "Количество пикселей"</li>
  <li>Чтобы получить гистограммы, нажмите "Гистограмма по каналам"</li>
</ol>
