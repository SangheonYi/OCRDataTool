# OCRDataTool
detection, recognition two stage 모델의 dataset 검수 도구
1. 검수에 필요한 데이터만 뽑아 종합해서 볼 수 있다.
2. detection, recognition label, inference 결과 , 이미지 data 필요
* detection, recognition label은 ppocr 학습 label 양식과 같다.
* inference result format 예시:
```
progress: 32/917491 path: Z:\home\sayi\workspace\OCR\TrainDataPreprocess\PDFPreprocess\cropped/&#65378;어린이 통학로 교통안전 기본계획&#65379; 용역 중간보고회 결과보고/0_32_.png
result len: 3 gt len: 3
result:	여린이
gt:		어린이

progress: 34/917491 path: Z:\home\sayi\workspace\OCR\TrainDataPreprocess\PDFPreprocess\cropped/&#65378;어린이 통학로 교통안전 기본계획&#65379; 용역 중간보고회 결과보고/0_34_.png
result len: 4 gt len: 4
result:	교통인전
gt:		교통안전

progress: 37/917491 path: Z:\home\sayi\workspace\OCR\TrainDataPreprocess\PDFPreprocess\cropped/&#65378;어린이 통학로 교통안전 기본계획&#65379; 용역 중간보고회 결과보고/0_37_.png
result len: 5 gt len: 5
result:	중간보교회
gt:		중간보고회
```
3. image index 탐색, 경로 copy 등 단축키 사용 가능
4. 검수한 이미지 index 저장으로 이어서 검수 가능
5. gt, image 경로로 필터링
![Untitled](https://github.com/SangheonYi/OCRDataTool/assets/16645988/21dd4aaa-ac22-4e96-b8ff-635cfde3c943)

