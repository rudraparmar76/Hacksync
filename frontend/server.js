import express from 'express';
import cors from 'cors';
import multer from 'multer';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import { v2 as cloudinary } from 'cloudinary';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = 5000;

// Configure Cloudinary
cloudinary.config({ 
  cloud_name: 'dier5yom4', 
  api_key: '613946922179936', 
  api_secret: process.env.CLOUDINARY_API_SECRET || 'your_api_secret_here'
});
// Enable CORS
app.use(cors());
app.use(express.json({ limit: '500mb' }));
app.use(express.urlencoded({ limit: '500mb', extended: true }));

// Configuration
const UPLOAD_FOLDER = path.join(__dirname, 'uploads');
const ALLOWED_EXTENSIONS = ['txt', 'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif'];
// No file size limit

// Create uploads folder if it doesn't exist
if (!fs.existsSync(UPLOAD_FOLDER)) {
  fs.mkdirSync(UPLOAD_FOLDER, { recursive: true });
}

// Configure multer for file uploads (memory storage for Cloudinary)
const storage = multer.memoryStorage();

const fileFilter = (req, file, cb) => {
  const ext = path.extname(file.originalname).toLowerCase().slice(1);
  if (ALLOWED_EXTENSIONS.includes(ext)) {
    cb(null, true);
  } else {
    cb(new Error(`File type .${ext} not allowed`), false);
  }
};

const upload = multer({
  storage: storage,
  fileFilter: fileFilter
  // No file size limit
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString()
  });
});

// File upload endpoint with Cloudinary
app.post('/api/upload', upload.array('files', 10), async (req, res) => {
  try {
    if (!req.files || req.files.length === 0) {
      return res.status(400).json({ error: 'No files provided' });
    }

    // Upload each file to Cloudinary with chunked upload for large files
    const uploadPromises = req.files.map(file => {
      return new Promise((resolve, reject) => {
        const uploadStream = cloudinary.uploader.upload_stream(
          {
            folder: 'ather-uploads',
            resource_type: 'auto',
            public_id: `${Date.now()}_${file.originalname.replace(/[^a-zA-Z0-9._-]/g, '_')}`,
            chunk_size: 6000000, // 6MB chunks for large files
            timeout: 120000 // 2 minutes timeout
          },
          (error, result) => {
            if (error) {
              reject(error);
            } else {
              resolve({
                original_name: file.originalname,
                url: result.secure_url,
                public_id: result.public_id,
                size: file.size,
                type: file.mimetype,
                format: result.format
              });
            }
          }
        );
        uploadStream.end(file.buffer);
      });
    });

    const uploadedFiles = await Promise.all(uploadPromises);

    res.json({
      success: true,
      files: uploadedFiles,
      count: uploadedFiles.length
    });
  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Chat message endpoint
app.post('/api/chat/message', (req, res) => {
  try {
    const { message, files = [] } = req.body;

    // Mock AI response - integrate with your AI service
    const response = {
      reply: `Received your message: ${message}`,
      agents: {
        support: 'Analysis in progress...',
        opposing: 'Critique pending...',
        synthesizer: 'Synthesis scheduled...'
      }
    };

    if (files.length > 0) {
      response.files_processed = files.length;
    }

    res.json(response);
  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Error handling middleware
app.use((error, req, res, next) => {
  console.error('Server error:', error);
  res.status(500).json({ error: error.message });
});

// Start server
app.listen(PORT, () => {
  console.log('🚀 ATHER Backend Server Starting...');
  console.log(`📁 Upload folder: ${UPLOAD_FOLDER}`);
  console.log(`🌐 Server running on http://localhost:${PORT}`);
  console.log(`� Allowed extensions: ${ALLOWED_EXTENSIONS.join(', ')}`);
  console.log('📝 No file size limit - Upload files of any size');
});
