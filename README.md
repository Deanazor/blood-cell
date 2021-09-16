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

## Or you can just simply pull the image
Pull docker image:

```bash
  docker pull deanazor/blood-cell
```

## Now, you can run the container
Run image :

```bash
  docker run --rm -p 8080:8080 deanazor/blood-cell
```

# Result

## Input :
![uninfected](coba/test_1.png)

## Output :
```python
{
    "filename": "2021-09-16_17:02:16-test_1.png",
    "result": [
        {
            "confidence": "0.9894008",
            "label": "uninfected"
        }
    ],
    "status": "OK"
}
```

## Input : 
![uninfected](coba/test_2.png)

## Output : 
```python
{
    "filename": "2021-09-16_17:02:44-test_2.png",
    "result": [
        {
            "confidence": "1.0",
            "label": "parasitised"
        }
    ],
    "status": "OK"
}
```