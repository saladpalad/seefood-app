import UIKit
import CoreML
import Vision
import SVProgressHUD


class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    
    let imagePicker = UIImagePickerController()
    
    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var cameraButton: UIBarButtonItem!
    @IBOutlet weak var topBarImageView: UIImageView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        imagePicker.delegate = self
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        
        cameraButton.isEnabled = false
        SVProgressHUD.show()
        
        if let userPickedImage = info[UIImagePickerController.InfoKey.originalImage] as? UIImage {
            imageView.image = userPickedImage
            if let ciimage = CIImage(image: userPickedImage) {
                detect(image: ciimage)
            } else {
                print("Error converting UIImage to CIImage")
            }
        } else {
            print("Error with selecting the image")
        }
        picker.dismiss(animated: true, completion: nil)
    }
    
    /*
    func detect(image: CIImage) {
        guard let modelPath = Bundle.main.path(forResource: "Resnet50", ofType: "mlmodel") else {
            print("Error: Could not find model.")
            return
        }

        let modelURL = URL(fileURLWithPath: modelPath)
        
        do {
            let model = try VNCoreMLModel(for: MLModel(contentsOf: modelURL))
            // Use the model for inference here
        } catch {
            print("Error loading Core ML model:", error)
        }
    }
     */
    
    func customizeNavigationTitle() {
        let titleLabel = UILabel()
        titleLabel.text = "Title"
        titleLabel.textAlignment = .center
        titleLabel.textColor = .white
        titleLabel.font = UIFont.boldSystemFont(ofSize: 24) // Adjust font size as needed
        
        let titleView = UIView(frame: CGRect(x: 0, y: 0, width: UIScreen.main.bounds.width, height: 60)) // Adjust height as needed
        titleView.addSubview(titleLabel)
        
        // Adjust title label frame if needed
        titleLabel.translatesAutoresizingMaskIntoConstraints = false
        titleLabel.centerXAnchor.constraint(equalTo: titleView.centerXAnchor).isActive = true
        titleLabel.centerYAnchor.constraint(equalTo: titleView.centerYAnchor).isActive = true
        
        self.navigationItem.titleView = titleView
    }
    
    
    func detect(image: CIImage) {
        let model = try? VNCoreMLModel(for: Resnet50().model)
        
        let request = VNCoreMLRequest(model: model!) { (request, error) in
            guard let results = request.results as? [VNClassificationObservation], let firstResult = results.first else {
                print("Unable to process image.")
                return
            }
            
            // re-enable camera after image is classified
            DispatchQueue.main.async{
                self.cameraButton.isEnabled = true
                SVProgressHUD.dismiss()
            }
            
            if firstResult.identifier.contains("hotdog") {
                DispatchQueue.main.async {
                    self.navigationItem.title = "Hotdog"
                    self.navigationController?.navigationBar.backgroundColor = UIColor.green
                    self.navigationController?.navigationBar.isTranslucent = false
                    self.topBarImageView.image = UIImage(named:"hotdog_v2")
                }
            } else {
                DispatchQueue.main.async {
                    self.navigationItem.title = "Not Hotdog"
                    self.navigationController?.navigationBar.backgroundColor = UIColor.red
                    self.navigationController?.navigationBar.isTranslucent = false
                    self.topBarImageView.image = UIImage(named:"not_hotdog")
                }
            }
        }
        
        let handler = VNImageRequestHandler(ciImage: image)
        do {
            try handler.perform([request])
        } catch {
            print("Error performing request: \(error.localizedDescription)")
        }
    }
    
    @IBAction func cameraTapped(_ sender: UIBarButtonItem) {
        imagePicker.sourceType = .camera
        imagePicker.allowsEditing = false
        present(imagePicker, animated: true, completion: nil)
    }   
}
