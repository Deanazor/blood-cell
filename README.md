# Blood Cell Detection

This is a simple classification model using pytorch to detect malaria-infected blood cell

## How to run

Clone repository :

```bash
  git clone https://github.com/Deanazor/blood-cell.git
```

Go to repository folder :

```bash
  cd blood-cell
```

Build docker image :

```bash
  docker build -t deanazor/blood-cell .
```

Run image :

```bash
  docker run --rm -p 8080:8080 deanazor/blood-cell
```