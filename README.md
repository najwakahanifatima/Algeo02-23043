![Logo of the project](https://raw.githubusercontent.com/jehna/readme-best-practices/master/sample-logo.png)

# MuseIc
> Find your music

Sebuah website yang dapat menerima input lagu, gambar album, dan file humming dan mendeteksi nama dari lagu tersebut. 

## Installing / Getting started
Anda perlu menginstall pip dan Node.js.
Setelah itu, install package package di bawah ini dengan run kode :
```shell
pip install pillow
pip install mido
pip install numpy
pip install scipy
pip install rarfile
pip install zipfile
pip install uvicorn
npm install react
npm install next
```
### Initial Configuration

Buka 2 terminal.
Di terminal pertama, navigasi ke folder backend, lalu jalankan API.
```shell
cd src/backend
uvicorn app:app --reload
```
Di terminal ke dua, navigasi ke folder frontend, lalu jalankan interface.

```shell
cd src/frontend
npm run dev
```
Jika port tidak terpakai, website akan dijalankan di http://localhost:3000. CTRL+klik link tersebut di terminal Anda. 


## Developing

### Building


### Deploying / Publishing

In case there's some step you have to take that publishes this project to a
server, this is the right time to state it.

```shell
packagemanager deploy awesome-project -s server.com -u username -p password
```

And again you'd need to tell what the previous code actually does.

## Features

* Query by Humming
* Album Finder

## Configuration

Here you should write what are all of the configurations a user can enter when
using the project.

#### Argument 1
Type: `String`  
Default: `'default value'`

State what an argument does and how you can use it. If needed, you can provide
an example below.

Example:
```bash
awesome-project "Some other value"  # Prints "You're nailing this readme!"
```

#### Argument 2
Type: `Number|Boolean`  
Default: 100

Copy-paste as many of these as you need.

## Contributing
Apabila Anda ingin berkontribusi dalam projek ini, silakan fork repository ini dan gunakan feature branch. Pull requests akan diterima dengan hangat.

## Links


- Repository: https://github.com/najwakahanifatima/Algeo02-23043
- Issue tracker: https://github.com/your/awesome-project/issues
  - In case of sensitive bugs like security vulnerabilities, please contact
    
    emaiiillll

## Licensing

"The code in this project is licensed under MIT license."