from ml import train_and_save


if __name__ == "__main__":
    result = train_and_save()
    print(f"Model saved to {result['model_path']}")
    print(f"Best accuracy: {result['accuracy']:.3f}")
    print(f"Selected model: {result['type']}")
