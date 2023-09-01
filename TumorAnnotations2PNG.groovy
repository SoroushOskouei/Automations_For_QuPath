import qupath.lib.images.servers.LabeledImageServer

// Function to process each image data
def processImageData(imageData) {
    // Define output path (relative to project)
    def name = GeneralTools.getNameWithoutExtension(imageData.getServer().getMetadata().getName())
    name = name.replaceAll(".vsi - 40x", "")  // Adjust the name format
    //name = name.replaceAll(" ", "_")  // Adjust the name format
    def pathOutput = buildFilePath("Target/path/")
    mkdirs(pathOutput)

    // Define the downsampling factor
    double downsample = 32

    // Create an ImageServer where the pixels are derived from Tumor annotations
    def labelServer = new LabeledImageServer.Builder(imageData)
        .backgroundLabel(0, ColorTools.BLACK) // Specify background label as black
        .downsample(downsample)    // Set the resolution
        .addLabel('Tumor', 1)    // Set Tumor label as white
        .multichannelOutput(false) // Set to false for binary image
        .build()

    // Export entire image at downsampled resolution with Tumor annotations
    def region = RegionRequest.createInstance(labelServer.getPath(), downsample, 0, 0, labelServer.getWidth(), labelServer.getHeight())
    def outputPath = buildFilePath(pathOutput,name + '.png')
    writeImageRegion(labelServer, region, outputPath)
}

// Iterate over all images in the project and process them
def project = getProject()
if (project == null) {
    print("No project open!")
    return
}

for (entry in project.getImageList()) {
    def imageData = entry.readImageData()
    processImageData(imageData)
}
