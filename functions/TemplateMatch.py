import numpy as np
import cv2


def check_square(points) -> bool:
    if abs(points[0][0][1] - points[1][0][1]) < 380 or abs(points[0][0][0] - points[2][0][0]) < 380:
        return False
    if (abs(points[0][0][0] - points[1][0][0]) > 50 or abs(points[0][0][1] - points[3][0][1]) > 50 or
            abs(points[1][0][1] - points[2][0][1]) > 50 or abs(points[2][0][0] - points[3][0][0]) > 50):
        return False
    return True


def match_template(main_image, template_image, threshold: float = 1):
    # # 读取图片
    # main_image = cv2.imread(main_image_path, cv2.IMREAD_GRAYSCALE)
    # template_image = cv2.imread(template_image_path, cv2.IMREAD_GRAYSCALE)

    # 使用SIFT检测特征点并计算描述符
    sift = cv2.SIFT.create()
    keypoints_main, descriptors_main = sift.detectAndCompute(main_image, None)
    keypoints_template, descriptors_template = sift.detectAndCompute(template_image, None)

    if descriptors_main is None:
        # print('No matches found: descriptors_main is None')
        return False
    if descriptors_template is not None and descriptors_template.dtype != 'float32':
        descriptors_template = descriptors_template.astype('float32')
    if descriptors_main is not None and descriptors_main.dtype != 'float32':
        descriptors_main = descriptors_main.astype('float32')

    # 暴力特征点匹配
    bf = cv2.BFMatcher(cv2.NORM_L2)
    matches = bf.knnMatch(descriptors_template, descriptors_main, k=2)

    good_matches = []
    for match in matches:
        if len(match) == 2:
            for m, n in matches:
                if m.distance < threshold * n.distance:
                    good_matches.append(m)
    # for m, n in matches:
    #     if m.distance < threshold * n.distance:
    #         good_matches.append(m)

    # print(f'Total matches: {len(matches)}')
    # print(f'Good matches: {len(good_matches)}')

    if len(good_matches) > 4:
        # 提取匹配点坐标
        src_pts = np.float32([keypoints_template[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints_main[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # 计算变换矩阵
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        # matches_mask = mask.ravel().tolist()

        if M is None:
            # print('No matches found: M is None')
            return False
        h, w = template_image.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)

        # print(np.int32(dst))
        # print(np.int32(dst)[0][0][0])
        if len(dst) != 4 or check_square(dst) == False:
            # print('No matches found: Not Square')
            return False

        # 在大图上绘制匹配区域
        # main_image_with_matches = main_image.copy()
        # main_image_with_matches = cv2.polylines(main_image_with_matches, [np.int32(dst)], True, (255, 255, 255), 10,
        #                                         cv2.LINE_AA)

        # 显示匹配结果
        # height, width = main_image.shape
        # print(width, height)

        # cv2.namedWindow('Detected Template', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Detected Template', width * 1000 // height, 1000)
        # cv2.imshow('Detected Template', main_image_with_matches)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # averages = np.mean(dst.squeeze(), axis=0)
        # center_point = np.array(averages)
        # print(center_point)

        return True
    else:
        # print('No matches found: No Good Matches')
        return False


if __name__ == '__main__':
    # test graph
    main_path = './testfiles/test_main.jpg'
    template_path = './testfiles/template.png'
    # match_template(main_path, template_path)
    main_img = cv2.imread(main_path, cv2.IMREAD_GRAYSCALE)
    height, width = main_img.shape[:2]
    main_img = cv2.resize(main_img, (1000, height * 1000 // width), interpolation=cv2.INTER_LINEAR)
    template_img = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    r, g, b, a = cv2.split(template_img)
    rgba = np.hstack((r, g, b, a))
    template_img = cv2.cvtColor(a, cv2.COLOR_GRAY2BGR)
    template_img = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
    # template_img = cv2.cvtColor(template_img[:, :, :3], cv2.COLOR_BGR2GRAY)
    # cv2.imwrite('./testfiles/gray_template.png', template_img)
    # cv2.imshow('Main Image', main_img)
    # cv2.imshow('rgba', rgba)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    match_template(main_img, template_img)
