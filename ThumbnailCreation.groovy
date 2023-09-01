// Get the project
def project = QP.getProject()

// Define the downsample factor
def downsample = 32

// Loop through all images in the project
for (entry in project.getImageList()) {
    // Open the image
    def imageData = entry.readImageData()
    def server = imageData.getServer()

    // Request the entire image at the desired downsample
    def request = RegionRequest.createInstance(server.getPath(), downsample, 0, 0, server.getWidth(), server.getHeight())
    BufferedImage img = server.readRegion(request)

    // Define the output path (you might want to adjust this to your needs)
    def outputPath = "path/to/your/target/directory/" + entry.getImageName() + ".png"

    // Save the downsampled image as PNG or any format you desire
    javax.imageio.ImageIO.write(img, "PNG", new File(outputPath))

    // Print out progress
    print "Exported " + entry.getImageName() + "\n"
}

print "All images exported!"
