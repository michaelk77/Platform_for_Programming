<h1 align="center">Hi there, I'm <a href="https://github.com/michaelk77/" target="_blank">Michael</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
<h3 align="center">Computer science student, coder from Russia</h3>
Это мой проект по созданию платформы для программирования на python

Я понял что у многих моих знакомых и просто у людей связанных с программированием есть конкретная частая проблемма, в какой-то момент нет доступа к компьютеру, а онлайн компиляторы это просто ужас какой-то

Поэтому я сделал своего <a href="https://t.me/Py_mk_bot" target="_blank">бота</a> 

Там очень много всего полезного и интересного, для более подробного изучения добавил <a href="https://github.com/michaelk77/Platform_for_Programming/blob/main/Платформа%20для%20python%20tg.pptx" target="_blank">презентацию</a> в этот репозиторий
[![Typing SVG](https://readme-typing-svg.herokuapp.com?size=22&duration=3000&multiline=true&width=500&height=70&lines=%D0%9F%D0%BE+%D0%BC%D0%BE%D0%B5%D0%BC%D1%83+%D1%8D%D1%82%D0%BE+%D0%BF%D1%80%D0%BE%D1%81%D1%82%D0%BE+%D0%B2%D1%8B%D0%B3%D0%BB%D1%8F%D0%B4%D0%B8%D1%82+%D0%BF%D1%80%D0%B8%D0%BA%D0%BE%D0%BB%D1%8C%D0%BD%D0%BE;%D0%9D%D0%BE+%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82+%D0%B3%D0%BE%D1%80%D0%B0%D0%B7%D0%B4%D0%BE+%D0%BB%D1%83%D1%87%D1%88%D0%B5)](https://t.me/Py_mk_bot)

- uses: Platane/snk@v2
  with:
    # github user name to read the contribution graph from (**required**)
    # using action context var `github.repository_owner` or specified user
    github_user_name: ${{ github.repository_owner }}

    # list of files to generate.
    # one file per line. Each output can be customized with options as query string.
    #
    #  supported options:
    #  - palette:     A preset of color, one of [github, github-dark, github-light]
    #  - color_snake: Color of the snake
    #  - color_dots:  Coma separated list of dots color.
    #                 The first one is 0 contribution, then it goes from the low contribution to the highest.
    #                 Exactly 5 colors are expected.
    outputs: |
      dist/github-snake.svg
      dist/github-snake-dark.svg?palette=github-dark
      dist/ocean.gif?color_snake=orange&color_dots=#bfd6f6,#8dbdff,#64a1f4,#4b91f1,#3c7dd9
