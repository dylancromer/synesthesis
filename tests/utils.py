from synesthesis.utils import load_image_file, _save_image


def test_load_image_file():
    TEST_IMAGE = 'data/tests/test1.jpg'
    image = load_image_file(TEST_IMAGE)

    TEST_IMAGE_OUTFILE = 'data/tests/test1_out.jpg'
    _save_image(image, TEST_IMAGE_OUTFILE)
