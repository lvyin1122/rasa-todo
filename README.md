# Useful commands

## Generating data with Chatette

```
python -m chatette chatette\master.chatette -a rasa-md
```

## Evaluating the NLU model

```
rasa data split nlu
rasa test nlu
    --nlu train_test_split/test_data.yml
```

