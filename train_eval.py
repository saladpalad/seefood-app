import torch
from tqdm import tqdm
import numpy as np

def train(model, train_loader, val_loader, optimizer, criterion, device, num_epochs):

    model = model.to(device)
    
    history = {'train_loss': [], 'train_accuracy': [], 'val_loss': [], 'val_accuracy': []}
    
    for epoch in range(num_epochs):
        model.train() 
        
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        # Use tqdm to display a progress bar during training
        with tqdm(total=len(train_loader), desc=f'Epoch {epoch + 1}/{num_epochs}') as pbar:
            for inputs, labels, _ in train_loader:
                # Move inputs and labels to device
                inputs = inputs.float().to(device)
                labels = labels.to(device)
               
                # Zero out gradients
                optimizer.zero_grad()
              
                # Compute the logits and loss
                model = model.float()
                logits = model(inputs)
               
                loss = criterion(logits.float(), labels.long())

                # L1 Loss
                # l1_weight = 2e-4
                # l1_loss = l1_weight * model.compute_l1_loss()

                # loss += l1_loss

                # Backpropagate the loss
                loss.backward()

                # Update the weights
                optimizer.step()

                train_loss += loss.item()
                # Update the progress bar
                pbar.update(1)
                #pbar.set_postfix(loss=loss.item())
                
                _, predictions = torch.max(logits, dim=1)
                train_correct += (predictions == labels).sum().item()
                train_total += labels.size(0)
                
                pbar.set_postfix(loss=train_loss / train_total, accuracy=train_correct / train_total)

        # Evaluate the model on the validation set
        val_loss, val_accuracy = evaluate(model, val_loader, criterion, device)
        print(f'Validation set: Average loss = {val_loss:.4f}, Accuracy = {val_accuracy:.4f}')
       
        
        # Update history
        history['train_loss'].append(train_loss / train_total)
        history['train_accuracy'].append(train_correct / train_total)
        history['val_loss'].append(val_loss)
        history['val_accuracy'].append(val_accuracy)

    return history

def evaluate(model, test_loader, criterion, device):

    model.eval()  # Set model to evaluation mode
    #test_writer = SummaryWriter('logs/test')
    with torch.no_grad():
        total_loss = 0.0
        num_correct = 0
        num_samples = 0

        for inputs, labels, _ in test_loader:
            # Move inputs and labels to device
            inputs = inputs.float().to(device)
            labels = labels.to(device)
            #labels = torch.argmax(labels, dim=1)
            model = model.float()
            
            # Compute the logits and loss
            logits = model(inputs)
            loss = criterion(logits, labels.long())
            total_loss += loss.item()

            # Compute the accuracy
            _, predictions = torch.max(logits, dim=1)
            #print("predictions: ", predictions)
            #print("labels", labels)
            num_correct += (predictions == labels).sum().item()
            num_samples += len(inputs)

    # Compute the average loss and accuracy
    avg_loss = total_loss / len(test_loader)
    accuracy = num_correct / num_samples


    return avg_loss, accuracy