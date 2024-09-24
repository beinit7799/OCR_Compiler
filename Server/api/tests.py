# from django.test import TestCase

# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# from sklearn.metrics import precision_recall_curve
# import pytesseract
# from PIL import Image
# import os
# import string

# # Function to create a confusion matrix
# def create_confusion_matrix(ground_truth, recognized_text, labels):
#     label_to_index = {label: index for index, label in enumerate(labels)}
#     matrix = np.zeros((len(labels), len(labels)), dtype=int)
#     for gt_char, rec_char in zip(ground_truth, recognized_text):
#         gt_index = label_to_index.get(gt_char, -1)
#         rec_index = label_to_index.get(rec_char, -1)
#         if gt_index != -1 and rec_index != -1:
#             matrix[gt_index, rec_index] += 1
#     return matrix

# # Function to obtain recognized text from an image using Tesseract OCR
# def get_recognized_text(image_path):
#     try:
#         image = Image.open(image_path)
#         recognized_text = pytesseract.image_to_string(image).strip()
#         return recognized_text
#     except Exception as e:
#         print(f"Error processing {image_path}: {str(e)}")
#         return ""

# # Read the CSV file
# csv_path = 'D:/6th sem/project/OCRCompiler/Server/media/Data/test.csv'

# # Read CSV file ensuring header row is properly used
# df = pd.read_csv(csv_path, sep=',', engine='python', encoding='utf-8')

# # Ensure the expected columns are present
# expected_columns = ['Image', 'Text']
# if not set(expected_columns).issubset(df.columns):
#     raise ValueError("CSV file must contain 'Image' and 'Text' columns")

# # Define a comprehensive set of alphanumeric characters and symbols
# all_letters = string.ascii_letters  # A-Z, a-z
# all_digits = string.digits  # 0-9
# all_punctuation = string.punctuation  # All punctuation symbols
# # all_symbols = list("+-*/%= == != <> <= >= && || ! & | ^ ~ << >> += -= *= /= %= . , ; {} [] () ' \" \ # /* */ // ")
# # Combine all into a single list
# all_labels = list(all_letters) + list(all_digits) 

# # Get the directory of the CSV file
# csv_dir = os.path.dirname(csv_path)

# # Initialize lists to store metrics from each image
# all_conf_matrices = []
# all_precisions = []
# all_recalls = []


# # Process each row in the DataFrame
# for index, row in df.iterrows():
#     image_name = row['Image']
#     ground_truth = row['Text']
    
#     # Process the image
#     image_path = os.path.join(csv_dir, image_name)
#     recognized_text = get_recognized_text(image_path)
    
#     if recognized_text:
#         # Collect all unique characters for labels
#         # all_labels = sorted(set(ground_truth + recognized_text))
        
#         # Initialize confusion matrix
#         conf_matrix = create_confusion_matrix(ground_truth, recognized_text, all_labels)
#         all_conf_matrices.append(conf_matrix)
        
#         # Calculate precision and recall
#         y_true = [1 if gt == rec else 0 for gt, rec in zip(ground_truth, recognized_text)]
#         y_scores = [1 if rec in ground_truth else 0 for rec in recognized_text]
        
#         # Ensure the lengths of y_true and y_scores are the same by padding the shorter list
#         max_length = max(len(y_true), len(y_scores))
#         y_true.extend([0] * (max_length - len(y_true)))  # Padding y_true with 0s
#         y_scores.extend([0] * (max_length - len(y_scores)))  # Padding y_scores with 0s

#         precision, recall, _ = precision_recall_curve(y_true, y_scores)
#         all_precisions.append(precision)
#         all_recalls.append(recall)
#     else:
#         print(f"Recognition failed for image: {image_path}")

# # Aggregate confusion matrix
# combined_conf_matrix = np.sum(all_conf_matrices, axis=0)

# # Aggregate precision and recall
# combined_precision = np.mean(all_precisions, axis=0)
# combined_recall = np.mean(all_recalls, axis=0)

# # # Plot an example confusion matrix (first image processed)
# # if all_conf_matrices:
# #     plt.figure(figsize=(10, 10))
# #     plt.imshow(all_conf_matrices[0], cmap='Blues')
# #     plt.title('Confusion Matrix - First Image')
# #     plt.xlabel('Predicted')
# #     plt.ylabel('Actual')
# #     plt.xticks(ticks=np.arange(len(all_labels)), labels=all_labels, rotation=90)
# #     plt.yticks(ticks=np.arange(len(all_labels)), labels=all_labels)
# #     plt.colorbar()
# #     plt.savefig(f'confusion_matrix_image1.png')
# #     plt.show()

# # # Plot an example precision-recall curve (first image processed)
# # if all_precisions and all_recalls:
# #     plt.figure()
# #     plt.plot(all_recalls[0], all_precisions[0], marker='.')
# #     plt.xlabel('Recall')
# #     plt.ylabel('Precision')
# #     plt.title('Precision-Recall Curve - First Image')
# #     plt.savefig(f'precision_recall_curve_image1.png')
# #     plt.show()

# # Plot combined confusion matrix
# plt.figure(figsize=(15, 15))
# plt.imshow(combined_conf_matrix, cmap='Blues',interpolation='nearest')
# plt.title('Combined Confusion Matrix',fontsize=20)
# plt.xlabel('Predicted',fontsize=16)
# plt.ylabel('Actual',fontsize=16)
# plt.xticks(ticks=np.arange(len(all_labels)), labels=all_labels, rotation=90)
# plt.yticks(ticks=np.arange(len(all_labels)), labels=all_labels)
# plt.colorbar()
# plt.tight_layout()
# plt.savefig('media/figures/combined_confusion_matrix.png')
# plt.show()

# # Plot combined precision-recall curve
# plt.figure()
# plt.plot(combined_recall, combined_precision, marker='.')
# plt.xlabel('Recall',fontsize=14)
# plt.ylabel('Precision',fontsize=14)
# plt.title('Combined Precision-Recall Curve',fontsize=16)
# plt.savefig('media/figures/combined_precision_recall_curve.png')
# plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# from sklearn.metrics import precision_recall_curve, classification_report ,accuracy_score ,confusion_matrix
# import pytesseract
# from PIL import Image
# import os
# import string

# # Function to create a confusion matrix
# def create_confusion_matrix(ground_truth, recognized_text, labels):
#     label_to_index = {label: index for index, label in enumerate(labels)}
#     matrix = np.zeros((len(labels), len(labels)), dtype=int)
#     for gt_char, rec_char in zip(ground_truth, recognized_text):
#         gt_index = label_to_index.get(gt_char, -1)
#         rec_index = label_to_index.get(rec_char, -1)
#         if gt_index != -1 and rec_index != -1:
#             matrix[gt_index, rec_index] += 1
#     return matrix

# # Function to obtain recognized text from an image using Tesseract OCR
# def get_recognized_text(image_path):
#     try:
#         image = Image.open(image_path)
#         recognized_text = pytesseract.image_to_string(image).strip()
#         return recognized_text
#     except Exception as e:
#         print(f"Error processing {image_path}: {str(e)}")
#         return ""

# # Read the CSV file
# csv_path = 'D:/6th sem/project/OCRCompiler/Server/media/Data/ocr.csv'

# # Read CSV file ensuring header row is properly used
# df = pd.read_csv(csv_path, sep=',', engine='python', encoding='utf-8')

# # Ensure the expected columns are present
# expected_columns = ['Image', 'Text']
# if not set(expected_columns).issubset(df.columns):
#     raise ValueError("CSV file must contain 'Image' and 'Text' columns")

# # Define a comprehensive set of alphanumeric characters and symbols (excluding whitespace)
# all_letters = string.ascii_letters  # A-Z, a-z
# all_digits = string.digits  # 0-9
# all_punctuation = string.punctuation  # All punctuation symbols
# all_labels = list(all_letters) + list(all_digits) + list(all_punctuation)
# # Get the directory of the CSV file
# csv_dir = os.path.dirname(csv_path)

# # Initialize lists to store metrics from each image
# all_conf_matrices = []
# all_y_true = []
# all_y_pred = []

# # Process each row in the DataFrame
# for index, row in df.iterrows():
#     image_name = row['Image']
#     ground_truth = row['Text']
    
#     # Process the image
#     image_dir = 'D:/6th sem/project/OCRCompiler/Server/media/Test/'
#     image_path = os.path.join(image_dir, image_name)
#     recognized_text = get_recognized_text(image_path)
    
#     if recognized_text:
#         # Pad the shorter sequence to match lengths
#         max_length = max(len(ground_truth), len(recognized_text))
#         ground_truth = ground_truth.ljust(max_length)
#         recognized_text = recognized_text.ljust(max_length)
        
#         # Initialize confusion matrix
#         conf_matrix = create_confusion_matrix(ground_truth, recognized_text, all_labels)
#         all_conf_matrices.append(conf_matrix)
        
#         # Collect data for classification report
#         all_y_true.extend(list(ground_truth))
#         all_y_pred.extend(list(recognized_text))
#     else:
#         print(f"Recognition failed for image: {image_path}")

# # Aggregate confusion matrix
# combined_conf_matrix = np.sum(all_conf_matrices, axis=0)

# # Plot combined confusion matrix
# plt.figure(figsize=(20, 20))
# plt.imshow(combined_conf_matrix, cmap='Blues', interpolation='nearest')
# plt.title('Combined Confusion Matrix', fontsize=18)
# plt.xlabel('Predicted', fontsize=16)
# plt.ylabel('Actual', fontsize=16)
# plt.xticks(ticks=np.arange(len(all_labels)), labels=all_labels, rotation=90, fontsize=10)
# plt.yticks(ticks=np.arange(len(all_labels)), labels=all_labels, fontsize=10)
# plt.colorbar()
# plt.tight_layout()
# plt.savefig('media/figures/combined_confusion_matrix.png')
# plt.show()

# # Generate and print classification report
# accuracy = accuracy_score(all_y_true, all_y_pred)
# report = classification_report(all_y_true, all_y_pred, labels=all_labels, zero_division=0, output_dict=False, target_names=all_labels)
# print(report)
# print(f"Accuracy: {accuracy:.3f}\n")
# # Calculate accuracy


# # Calculate combined precision and recall for all samples
# y_true_binary = [1 if gt == rec else 0 for gt, rec in zip(all_y_true, all_y_pred)]
# y_scores_binary = [1 if rec in all_y_true else 0 for rec in all_y_pred]

# precision, recall, _ = precision_recall_curve(y_true_binary, y_scores_binary)

# # Plot combined precision-recall curve
# plt.figure()
# plt.plot(recall, precision, marker='.')
# plt.xlabel('Recall', fontsize=14)
# plt.ylabel('Precision', fontsize=14)
# plt.title('Combined Precision-Recall Curve', fontsize=16)
# plt.savefig('media/figures/combined_precision_recall_curve.png')
# plt.show()

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import precision_recall_curve, classification_report, accuracy_score, confusion_matrix
import pytesseract
from PIL import Image
import os
import string

# Function to create a confusion matrix
def create_confusion_matrix(ground_truth, recognized_text, labels):
    label_to_index = {label: index for index, label in enumerate(labels)}
    matrix = np.zeros((len(labels), len(labels)), dtype=int)
    for gt_char, rec_char in zip(ground_truth, recognized_text):
        gt_index = label_to_index.get(gt_char, -1)
        rec_index = label_to_index.get(rec_char, -1)
        if gt_index != -1 and rec_index != -1:
            matrix[gt_index, rec_index] += 1
    return matrix

# Function to obtain recognized text from an image using Tesseract OCR
def get_recognized_text(image_path, lang='eng'):
    try:
        image = Image.open(image_path)
        config = "--oem 3 --psm 6"
        recognized_text = pytesseract.image_to_string(image, config=config, lang=lang).strip()
        return recognized_text
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return ""

# Read the CSV file
csv_path = 'D:/6th sem/project/OCRCompiler/Server/media/Data/ocr.csv'
df = pd.read_csv(csv_path, sep=',', engine='python', encoding='utf-8')

# Ensure the expected columns are present
expected_columns = ['Image', 'Text']
if not set(expected_columns).issubset(df.columns):
    raise ValueError("CSV file must contain 'Image' and 'Text' columns")

# Define a comprehensive set of alphanumeric characters and symbols
all_letters = string.ascii_letters  # A-Z, a-z
all_digits = string.digits  # 0-9
all_punctuation = string.punctuation  # All punctuation symbols
all_labels = list(all_letters) + list(all_digits) + list(all_punctuation)

# Initialize lists to store metrics from each image
all_conf_matrices = []
all_y_true = []
all_y_pred = []

# Process each row in the DataFrame
for index, row in df.iterrows():
    image_name = row['Image']
    ground_truth = row['Text']
    
    # Process the image
    image_dir = 'D:/6th sem/project/OCRCompiler/Server/media/Output/'
    image_path = os.path.join(image_dir, image_name)
    recognized_text = get_recognized_text(image_path)
    
    if recognized_text:
        # Pad the shorter sequence to match lengths
        max_length = max(len(ground_truth), len(recognized_text))
        ground_truth = ground_truth.ljust(max_length)
        recognized_text = recognized_text.ljust(max_length)
        
        # Initialize confusion matrix
        conf_matrix = create_confusion_matrix(ground_truth, recognized_text, all_labels)
        all_conf_matrices.append(conf_matrix)
        
        # Collect data for classification report
        all_y_true.extend(list(ground_truth))
        all_y_pred.extend(list(recognized_text))
    else:
        print(f"Recognition failed for image: {image_path}")

# Aggregate confusion matrix
combined_conf_matrix = np.sum(all_conf_matrices, axis=0)

# Plot combined confusion matrix
plt.figure(figsize=(20, 20))
plt.imshow(combined_conf_matrix, cmap='Blues', interpolation='nearest')
plt.title('Combined Confusion Matrix', fontsize=18)
plt.xlabel('Predicted', fontsize=16)
plt.ylabel('Actual', fontsize=16)
plt.xticks(ticks=np.arange(len(all_labels)), labels=all_labels, rotation=90, fontsize=10)
plt.yticks(ticks=np.arange(len(all_labels)), labels=all_labels, fontsize=10)
plt.colorbar()
plt.tight_layout()
plt.savefig('media/figures/combined_confusion_matrix.png')
plt.show()

# Generate and print classification report
accuracy = accuracy_score(all_y_true, all_y_pred)
report = classification_report(all_y_true, all_y_pred, labels=all_labels, zero_division=0, output_dict=False, target_names=all_labels)
print(report)
print(f"Accuracy: {accuracy:.3f}\n")

# Calculate combined precision and recall for all samples
y_true_binary = [1 if gt == rec else 0 for gt, rec in zip(all_y_true, all_y_pred)]
y_scores_binary = [1 if rec in all_y_true else 0 for rec in all_y_pred]

precision, recall, _ = precision_recall_curve(y_true_binary, y_scores_binary)

# Plot combined precision-recall curve
plt.figure()
plt.plot(recall, precision, marker='.')
plt.xlabel('Recall', fontsize=14)
plt.ylabel('Precision', fontsize=14)
plt.title('Combined Precision-Recall Curve', fontsize=16)
plt.savefig('media/figures/combined_precision_recall_curve.png')
plt.show()
