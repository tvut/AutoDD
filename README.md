# AutoDD
Automatically does the "due diligence" for you. 

If you want to know what stocks people are talking about in r/pennystocks over 
at Reddit, this is the tool for you. 

## Installation
The ``Pipfile`` is broken. Instead just use pip to install ``psaw`` and ``bs4`` into your python environment. You might also need to install ``lxml`` and ``requests``.

## Running
Simply type in:

    python3 AutoDD.py

It will run through the all of the posts in the last couple days and pick out valid stocks and find their price and % change in the last day from Yahoo finance. Output will be put in the current directory in an html file called ``out.html``.

## License

    AutoDD - Automatically does the "due diligence" for you. 
    Copyright (C) 2020  Fufu Fang

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
