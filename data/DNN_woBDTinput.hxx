//Code generated automatically by TMVA for Inference of Model file [DNN_woBDTinput.onnx] at [Tue Jul 11 12:13:27 2023] 

#ifndef TMVA_SOFIE_DNN_WOBDTINPUT
#define TMVA_SOFIE_DNN_WOBDTINPUT

#include<algorithm>
#include<vector>
#include "TMVA/SOFIE_common.hxx"
#include <fstream>

namespace TMVA_SOFIE_DNN_woBDTinput{
namespace BLAS{
	extern "C" void sgemv_(const char * trans, const int * m, const int * n, const float * alpha, const float * A,
	                       const int * lda, const float * X, const int * incx, const float * beta, const float * Y, const int * incy);
	extern "C" void sgemm_(const char * transa, const char * transb, const int * m, const int * n, const int * k,
	                       const float * alpha, const float * A, const int * lda, const float * B, const int * ldb,
	                       const float * beta, float * C, const int * ldc);
}//BLAS
struct Session {
std::vector<float> fTensor_linearrelustack8bias = std::vector<float>(1);
float * tensor_linearrelustack8bias = fTensor_linearrelustack8bias.data();
std::vector<float> fTensor_linearrelustack8weight = std::vector<float>(4);
float * tensor_linearrelustack8weight = fTensor_linearrelustack8weight.data();
std::vector<float> fTensor_linearrelustack6weight = std::vector<float>(32);
float * tensor_linearrelustack6weight = fTensor_linearrelustack6weight.data();
std::vector<float> fTensor_linearrelustack4bias = std::vector<float>(8);
float * tensor_linearrelustack4bias = fTensor_linearrelustack4bias.data();
std::vector<float> fTensor_linearrelustack2bias = std::vector<float>(12);
float * tensor_linearrelustack2bias = fTensor_linearrelustack2bias.data();
std::vector<float> fTensor_linearrelustack2weight = std::vector<float>(288);
float * tensor_linearrelustack2weight = fTensor_linearrelustack2weight.data();
std::vector<float> fTensor_linearrelustack4weight = std::vector<float>(96);
float * tensor_linearrelustack4weight = fTensor_linearrelustack4weight.data();
std::vector<float> fTensor_linearrelustack0bias = std::vector<float>(24);
float * tensor_linearrelustack0bias = fTensor_linearrelustack0bias.data();
std::vector<float> fTensor_linearrelustack6bias = std::vector<float>(4);
float * tensor_linearrelustack6bias = fTensor_linearrelustack6bias.data();
std::vector<float> fTensor_linearrelustack0weight = std::vector<float>(816);
float * tensor_linearrelustack0weight = fTensor_linearrelustack0weight.data();
std::vector<float> fTensor_linearrelustacklinearrelustack7Reluoutput0 = std::vector<float>(4);
float * tensor_linearrelustacklinearrelustack7Reluoutput0 = fTensor_linearrelustacklinearrelustack7Reluoutput0.data();
std::vector<float> fTensor_linearrelustacklinearrelustack6Gemmoutput0 = std::vector<float>(4);
float * tensor_linearrelustacklinearrelustack6Gemmoutput0 = fTensor_linearrelustacklinearrelustack6Gemmoutput0.data();
std::vector<float> fTensor_19 = std::vector<float>(1);
float * tensor_19 = fTensor_19.data();
std::vector<float> fTensor_linearrelustacklinearrelustack5Reluoutput0 = std::vector<float>(8);
float * tensor_linearrelustacklinearrelustack5Reluoutput0 = fTensor_linearrelustacklinearrelustack5Reluoutput0.data();
std::vector<float> fTensor_linearrelustacklinearrelustack4Gemmoutput0 = std::vector<float>(8);
float * tensor_linearrelustacklinearrelustack4Gemmoutput0 = fTensor_linearrelustacklinearrelustack4Gemmoutput0.data();
std::vector<float> fTensor_linearrelustacklinearrelustack3Reluoutput0 = std::vector<float>(12);
float * tensor_linearrelustacklinearrelustack3Reluoutput0 = fTensor_linearrelustacklinearrelustack3Reluoutput0.data();
std::vector<float> fTensor_linearrelustacklinearrelustack2Gemmoutput0 = std::vector<float>(12);
float * tensor_linearrelustacklinearrelustack2Gemmoutput0 = fTensor_linearrelustacklinearrelustack2Gemmoutput0.data();
std::vector<float> fTensor_linearrelustacklinearrelustack1Reluoutput0 = std::vector<float>(24);
float * tensor_linearrelustacklinearrelustack1Reluoutput0 = fTensor_linearrelustacklinearrelustack1Reluoutput0.data();
std::vector<float> fTensor_linearrelustacklinearrelustack0Gemmoutput0 = std::vector<float>(24);
float * tensor_linearrelustacklinearrelustack0Gemmoutput0 = fTensor_linearrelustacklinearrelustack0Gemmoutput0.data();


Session(std::string filename ="") {
   if (filename.empty()) filename = "DNN_woBDTinput.dat";
   std::ifstream f;
   f.open(filename);
   if (!f.is_open()){
      throw std::runtime_error("tmva-sofie failed to open file for input weights");
   }
   std::string tensor_name;
   int length;
   f >> tensor_name >> length;
   if (tensor_name != "tensor_linearrelustack8bias" ) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor name; expected name is tensor_linearrelustack8bias , read " + tensor_name;
      throw std::runtime_error(err_msg);
    }
   if (length != 1) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor size; expected size is 1 , read " + std::to_string(length) ;
      throw std::runtime_error(err_msg);
    }
    for (int i =0; i < length; ++i) 
       f >> tensor_linearrelustack8bias[i];
   f >> tensor_name >> length;
   if (tensor_name != "tensor_linearrelustack8weight" ) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor name; expected name is tensor_linearrelustack8weight , read " + tensor_name;
      throw std::runtime_error(err_msg);
    }
   if (length != 4) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor size; expected size is 4 , read " + std::to_string(length) ;
      throw std::runtime_error(err_msg);
    }
    for (int i =0; i < length; ++i) 
       f >> tensor_linearrelustack8weight[i];
   f >> tensor_name >> length;
   if (tensor_name != "tensor_linearrelustack6weight" ) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor name; expected name is tensor_linearrelustack6weight , read " + tensor_name;
      throw std::runtime_error(err_msg);
    }
   if (length != 32) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor size; expected size is 32 , read " + std::to_string(length) ;
      throw std::runtime_error(err_msg);
    }
    for (int i =0; i < length; ++i) 
       f >> tensor_linearrelustack6weight[i];
   f >> tensor_name >> length;
   if (tensor_name != "tensor_linearrelustack4bias" ) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor name; expected name is tensor_linearrelustack4bias , read " + tensor_name;
      throw std::runtime_error(err_msg);
    }
   if (length != 8) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor size; expected size is 8 , read " + std::to_string(length) ;
      throw std::runtime_error(err_msg);
    }
    for (int i =0; i < length; ++i) 
       f >> tensor_linearrelustack4bias[i];
   f >> tensor_name >> length;
   if (tensor_name != "tensor_linearrelustack2bias" ) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor name; expected name is tensor_linearrelustack2bias , read " + tensor_name;
      throw std::runtime_error(err_msg);
    }
   if (length != 12) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor size; expected size is 12 , read " + std::to_string(length) ;
      throw std::runtime_error(err_msg);
    }
    for (int i =0; i < length; ++i) 
       f >> tensor_linearrelustack2bias[i];
   f >> tensor_name >> length;
   if (tensor_name != "tensor_linearrelustack2weight" ) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor name; expected name is tensor_linearrelustack2weight , read " + tensor_name;
      throw std::runtime_error(err_msg);
    }
   if (length != 288) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor size; expected size is 288 , read " + std::to_string(length) ;
      throw std::runtime_error(err_msg);
    }
    for (int i =0; i < length; ++i) 
       f >> tensor_linearrelustack2weight[i];
   f >> tensor_name >> length;
   if (tensor_name != "tensor_linearrelustack4weight" ) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor name; expected name is tensor_linearrelustack4weight , read " + tensor_name;
      throw std::runtime_error(err_msg);
    }
   if (length != 96) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor size; expected size is 96 , read " + std::to_string(length) ;
      throw std::runtime_error(err_msg);
    }
    for (int i =0; i < length; ++i) 
       f >> tensor_linearrelustack4weight[i];
   f >> tensor_name >> length;
   if (tensor_name != "tensor_linearrelustack0bias" ) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor name; expected name is tensor_linearrelustack0bias , read " + tensor_name;
      throw std::runtime_error(err_msg);
    }
   if (length != 24) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor size; expected size is 24 , read " + std::to_string(length) ;
      throw std::runtime_error(err_msg);
    }
    for (int i =0; i < length; ++i) 
       f >> tensor_linearrelustack0bias[i];
   f >> tensor_name >> length;
   if (tensor_name != "tensor_linearrelustack6bias" ) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor name; expected name is tensor_linearrelustack6bias , read " + tensor_name;
      throw std::runtime_error(err_msg);
    }
   if (length != 4) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor size; expected size is 4 , read " + std::to_string(length) ;
      throw std::runtime_error(err_msg);
    }
    for (int i =0; i < length; ++i) 
       f >> tensor_linearrelustack6bias[i];
   f >> tensor_name >> length;
   if (tensor_name != "tensor_linearrelustack0weight" ) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor name; expected name is tensor_linearrelustack0weight , read " + tensor_name;
      throw std::runtime_error(err_msg);
    }
   if (length != 816) {
      std::string err_msg = "TMVA-SOFIE failed to read the correct tensor size; expected size is 816 , read " + std::to_string(length) ;
      throw std::runtime_error(err_msg);
    }
    for (int i =0; i < length; ++i) 
       f >> tensor_linearrelustack0weight[i];
   f.close();
}

std::vector<float> infer(float* tensor_onnxGemm0){

//--------- Gemm
   char op_0_transA = 'n';
   char op_0_transB = 't';
   int op_0_m = 1;
   int op_0_n = 24;
   int op_0_k = 34;
   float op_0_alpha = 1;
   float op_0_beta = 1;
   int op_0_lda = 34;
   int op_0_ldb = 34;
   std::copy(tensor_linearrelustack0bias, tensor_linearrelustack0bias + 24, tensor_linearrelustacklinearrelustack0Gemmoutput0);
   BLAS::sgemm_(&op_0_transB, &op_0_transA, &op_0_n, &op_0_m, &op_0_k, &op_0_alpha, tensor_linearrelustack0weight, &op_0_ldb, tensor_onnxGemm0, &op_0_lda, &op_0_beta, tensor_linearrelustacklinearrelustack0Gemmoutput0, &op_0_n);

//------ RELU
   for (int id = 0; id < 24 ; id++){
      tensor_linearrelustacklinearrelustack1Reluoutput0[id] = ((tensor_linearrelustacklinearrelustack0Gemmoutput0[id] > 0 )? tensor_linearrelustacklinearrelustack0Gemmoutput0[id] : 0);
   }

//--------- Gemm
   char op_2_transA = 'n';
   char op_2_transB = 't';
   int op_2_m = 1;
   int op_2_n = 12;
   int op_2_k = 24;
   float op_2_alpha = 1;
   float op_2_beta = 1;
   int op_2_lda = 24;
   int op_2_ldb = 24;
   std::copy(tensor_linearrelustack2bias, tensor_linearrelustack2bias + 12, tensor_linearrelustacklinearrelustack2Gemmoutput0);
   BLAS::sgemm_(&op_2_transB, &op_2_transA, &op_2_n, &op_2_m, &op_2_k, &op_2_alpha, tensor_linearrelustack2weight, &op_2_ldb, tensor_linearrelustacklinearrelustack1Reluoutput0, &op_2_lda, &op_2_beta, tensor_linearrelustacklinearrelustack2Gemmoutput0, &op_2_n);

//------ RELU
   for (int id = 0; id < 12 ; id++){
      tensor_linearrelustacklinearrelustack3Reluoutput0[id] = ((tensor_linearrelustacklinearrelustack2Gemmoutput0[id] > 0 )? tensor_linearrelustacklinearrelustack2Gemmoutput0[id] : 0);
   }

//--------- Gemm
   char op_4_transA = 'n';
   char op_4_transB = 't';
   int op_4_m = 1;
   int op_4_n = 8;
   int op_4_k = 12;
   float op_4_alpha = 1;
   float op_4_beta = 1;
   int op_4_lda = 12;
   int op_4_ldb = 12;
   std::copy(tensor_linearrelustack4bias, tensor_linearrelustack4bias + 8, tensor_linearrelustacklinearrelustack4Gemmoutput0);
   BLAS::sgemm_(&op_4_transB, &op_4_transA, &op_4_n, &op_4_m, &op_4_k, &op_4_alpha, tensor_linearrelustack4weight, &op_4_ldb, tensor_linearrelustacklinearrelustack3Reluoutput0, &op_4_lda, &op_4_beta, tensor_linearrelustacklinearrelustack4Gemmoutput0, &op_4_n);

//------ RELU
   for (int id = 0; id < 8 ; id++){
      tensor_linearrelustacklinearrelustack5Reluoutput0[id] = ((tensor_linearrelustacklinearrelustack4Gemmoutput0[id] > 0 )? tensor_linearrelustacklinearrelustack4Gemmoutput0[id] : 0);
   }

//--------- Gemm
   char op_6_transA = 'n';
   char op_6_transB = 't';
   int op_6_m = 1;
   int op_6_n = 4;
   int op_6_k = 8;
   float op_6_alpha = 1;
   float op_6_beta = 1;
   int op_6_lda = 8;
   int op_6_ldb = 8;
   std::copy(tensor_linearrelustack6bias, tensor_linearrelustack6bias + 4, tensor_linearrelustacklinearrelustack6Gemmoutput0);
   BLAS::sgemm_(&op_6_transB, &op_6_transA, &op_6_n, &op_6_m, &op_6_k, &op_6_alpha, tensor_linearrelustack6weight, &op_6_ldb, tensor_linearrelustacklinearrelustack5Reluoutput0, &op_6_lda, &op_6_beta, tensor_linearrelustacklinearrelustack6Gemmoutput0, &op_6_n);

//------ RELU
   for (int id = 0; id < 4 ; id++){
      tensor_linearrelustacklinearrelustack7Reluoutput0[id] = ((tensor_linearrelustacklinearrelustack6Gemmoutput0[id] > 0 )? tensor_linearrelustacklinearrelustack6Gemmoutput0[id] : 0);
   }

//--------- Gemm
   char op_8_transA = 'n';
   char op_8_transB = 't';
   int op_8_m = 1;
   int op_8_n = 1;
   int op_8_k = 4;
   float op_8_alpha = 1;
   float op_8_beta = 1;
   int op_8_lda = 4;
   int op_8_ldb = 4;
   std::copy(tensor_linearrelustack8bias, tensor_linearrelustack8bias + 1, tensor_19);
   BLAS::sgemm_(&op_8_transB, &op_8_transA, &op_8_n, &op_8_m, &op_8_k, &op_8_alpha, tensor_linearrelustack8weight, &op_8_ldb, tensor_linearrelustacklinearrelustack7Reluoutput0, &op_8_lda, &op_8_beta, tensor_19, &op_8_n);
	std::vector<float> ret (tensor_19, tensor_19 + 1);
	return ret;
}
};
} //TMVA_SOFIE_DNN_woBDTinput

#endif  // TMVA_SOFIE_DNN_WOBDTINPUT
